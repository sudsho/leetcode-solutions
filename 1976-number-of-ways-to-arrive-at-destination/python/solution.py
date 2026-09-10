import heapq
import itertools
import random
from typing import List, Tuple

MOD = 10**9 + 7


def oracle_ways(n: int, roads: List[List[int]]) -> int:
    """Shortest-path count with no priority queue anywhere in it.

    Floyd-Warshall for the distances, then the tight edges `dist[u] + w ==
    dist[v]` form a DAG ordered by distance (every weight is at least 1, so a
    predecessor is strictly closer) and the count is a sum over it. `O(n^3)`,
    and nothing in it can hold a stale entry, which is the point.
    """
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    adjacent: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in roads:
        dist[u][v] = dist[v][u] = min(dist[u][v], w)
        adjacent[u].append((v, w))
        adjacent[v].append((u, w))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    from_start = dist[0]
    ways = [0] * n
    ways[0] = 1
    for v in sorted(range(n), key=lambda x: from_start[x]):
        if v == 0 or from_start[v] == inf:
            continue
        ways[v] = sum(ways[u] for u, w in adjacent[v] if from_start[u] + w == from_start[v]) % MOD
    return ways[n - 1]


def dijkstra_count(
    n: int, roads: List[List[int]], skip_stale: bool = True, relax_from_key: bool = True
) -> Tuple[int, int, int]:
    """Counting Dijkstra, instrumented, with both switches exposed.

    Returns `(ways, scanned, stale_pops)`. `skip_stale` is the line
    `if d > dist[u]: continue`. `relax_from_key` picks what the relaxation adds
    the edge weight to: the popped key `d`, or the stored `dist[u]`. On every pop
    the guard lets through the two are equal, so with the guard in place the
    second switch cannot change anything - and without it they are different
    programs.
    """
    adjacent: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in roads:
        adjacent[u].append((v, w))
        adjacent[v].append((u, w))

    dist = [float("inf")] * n
    ways = [0] * n
    dist[0], ways[0] = 0, 1
    heap = [(0, 0)]
    scanned = stale = 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1
            if skip_stale:
                continue
        base = d if relax_from_key else dist[u]
        for v, w in adjacent[u]:
            scanned += 1
            candidate = base + w
            if candidate < dist[v]:
                dist[v] = candidate
                ways[v] = ways[u]
                heapq.heappush(heap, (candidate, v))
            elif candidate == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n - 1], scanned, stale


class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        """Number of shortest paths from 0 to n-1, mod 1e9+7.

        Picked to put the 9th's position under a line that already has a name.
        Two instances so far - the max in 1163's skip and the bucket clear in
        1345 - each a line no part of the correctness argument mentions and that
        is nevertheless the whole bound, and both nights asked whether the *line*
        has that property. `if d > dist[u]: continue` is the most familiar
        candidate there is. Every account of Dijkstra calls it an optimisation,
        and on plain distances deleting it leaves every answer alone.

        Counting is where that stops being a fact about the line. On every pop
        the guard lets through, `d == dist[u]`, so the relaxation can read
        either one and the choice is invisible. Take the guard away and it is
        not. A stale pop of `u` offering `d + w` offers strictly more than
        `dist[u] + w >= dist[v]` and changes nothing. Offering `dist[u] + w`
        re-reads every tight edge out of `u`, and a tight edge is an equality by
        definition, so each one adds `ways[u]` to its endpoint a second time.

        So the same deleted line is complexity-only in one program and
        correctness in the other, and the two programs are identical everywhere
        the line is present. Measured in `__main__`: over every graph on 4 nodes
        with weights up to 3 and 5 nodes with weights up to 2, the three variants
        that keep the guard or the key agree with a Floyd-Warshall oracle on all
        of them, and the fourth is wrong on 18 of 3954 and 90 of 57354. On the
        staircase the harmless deletion costs exactly `(n-1)(1 + n(n-1)/2)` scans
        against `n(n-1)`, and the harmful one answers 10404 at n = 10 where the
        truth is 1.

        The prediction I wrote down first was that the wrong version would hide
        at large weight ranges, where two different paths rarely tie. It does
        not hide there - 164 of 400 random graphs at weights up to 10^4 - because
        the equality it trips is not a tie between two paths. It is the edge that
        already counted, read again. The one place it is invisible is all
        weights equal: pops then come out in BFS order, nothing is improved after
        it is pushed, and there is no stale entry for the guard to catch.

        This keeps the guard and reads `d`, so either single deletion is safe.
        """
        adjacent: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        for u, v, w in roads:
            adjacent[u].append((v, w))
            adjacent[v].append((u, w))

        dist = [float("inf")] * n
        ways = [0] * n
        dist[0], ways[0] = 0, 1
        heap = [(0, 0)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in adjacent[u]:
                candidate = d + w
                if candidate < dist[v]:
                    dist[v] = candidate
                    ways[v] = ways[u]
                    heapq.heappush(heap, (candidate, v))
                elif candidate == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD
        return ways[n - 1]


def all_graphs(n: int, weights: Tuple[int, ...]):
    """Every graph on n labelled nodes with each pair absent or one of `weights`,
    keeping the ones where n-1 is reachable from 0."""
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product((0,) + weights, repeat=len(pairs)):
        roads = [[u, v, w] for (u, v), w in zip(pairs, choice) if w]
        seen, stack = {0}, [0]
        while stack:
            x = stack.pop()
            for u, v, _ in roads:
                for a, b in ((u, v), (v, u)):
                    if a == x and b not in seen:
                        seen.add(b)
                        stack.append(b)
        if n - 1 in seen:
            yield roads


def staircase(n: int) -> List[List[int]]:
    """Complete graph with w(i, j) = 2(j - i) - 1.

    Final distances are `dist[j] = j` along the unit chain, and popping `i`
    offers every later `j` the tentative `2j - i - 1`, strictly smaller than what
    `i - 1` offered. So node `j` is pushed once by each of `0..j-1` and carries
    `j - 1` stale entries.
    """
    return [[i, j, 2 * (j - i) - 1] for i in range(n) for j in range(i + 1, n)]


if __name__ == "__main__":
    solution = Solution()

    example = [[0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3], [6, 3, 3], [3, 5, 1],
               [6, 5, 1], [2, 5, 1], [0, 4, 5], [4, 6, 2]]
    cases = [
        (7, example, 4),
        (2, [[1, 0, 10]], 1),
        (1, [], 1),
        (4, [[0, 1, 1], [1, 3, 1], [0, 2, 1], [2, 3, 1]], 2),
    ]
    print("answers")
    for n, roads, expected in cases:
        got = solution.countPaths(n, roads)
        assert got == expected == oracle_ways(n, roads), (n, roads, got, expected)
        print(f"  n={n}  ways={got}")

    variants = {
        "guard, reads d      ": (True, True),
        "guard, reads dist[u]": (True, False),
        "no guard, reads d   ": (False, True),
        "no guard, dist[u]   ": (False, False),
    }

    print("\nall four variants against the oracle, exhaustively")
    for n, weights in ((4, (1, 2, 3)), (5, (1, 2))):
        wrong = {name: 0 for name in variants}
        graphs = with_stale = 0
        for roads in all_graphs(n, weights):
            truth = oracle_ways(n, roads)
            graphs += 1
            for name, (skip, from_key) in variants.items():
                ways, _, stale = dijkstra_count(n, roads, skip, from_key)
                wrong[name] += ways != truth
                if name.startswith("guard, reads d "):
                    with_stale += stale > 0
        print(f"  n={n} weights={weights}  {graphs} graphs, {with_stale} with a stale pop")
        for name, count in wrong.items():
            print(f"    {name}  wrong on {count}")
        assert wrong["guard, reads d      "] == wrong["guard, reads dist[u]"] == 0
        assert wrong["no guard, reads d   "] == 0

    print("\ncost of dropping the guard when it is harmless, on the staircase")
    for n in (10, 50, 100, 200):
        roads = staircase(n)
        ways_g, scan_g, stale_g = dijkstra_count(n, roads, True, True)
        ways_u, scan_u, stale_u = dijkstra_count(n, roads, False, True)
        assert ways_g == ways_u == oracle_ways(n, roads) == 1, n
        assert stale_g == stale_u == (n - 1) * (n - 2) // 2, (n, stale_g)
        assert scan_g == n * (n - 1), (n, scan_g)
        assert scan_u == (n - 1) * (1 + n * (n - 1) // 2), (n, scan_u)
        wrong_ways, _, _ = dijkstra_count(n, roads, False, False)
        print(
            f"  n={n:4d}  guarded={scan_g:7d}   unguarded={scan_u:9d}"
            f"   ratio={scan_u / scan_g:6.1f}   dist[u] version says {wrong_ways}"
        )

    print("\nrandom graphs, n=40, edge prob 0.3, 400 per weight range")
    rng = random.Random(1976)
    for top in (1, 2, 3, 5, 10, 100, 10**4):
        wrong = stale_graphs = 0
        ratios = []
        for _ in range(400):
            n = 40
            roads = [[u, v, rng.randint(1, top)] for u, v in itertools.combinations(range(n), 2)
                     if rng.random() < 0.3]
            truth, scan_g, stale = dijkstra_count(n, roads, True, True)
            _, scan_u, _ = dijkstra_count(n, roads, False, True)
            bad, _, _ = dijkstra_count(n, roads, False, False)
            stale_graphs += stale > 0
            wrong += bad != truth
            ratios.append(scan_u / scan_g)
        print(
            f"  w in [1, {top:5d}]  stale pops in {stale_graphs:3d}/400"
            f"   dist[u] version wrong on {wrong:3d}/400"
            f"   unguarded scan ratio {sum(ratios) / len(ratios):.2f}x"
        )
