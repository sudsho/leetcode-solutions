import heapq
import itertools
import random
import time
from collections import deque
from typing import List, Optional, Tuple

INF = float("inf")


def leave(t: int, change: int) -> int:
    """Earliest time a walker standing at a vertex from time t may leave it.

    Every signal turns green at 0, 2*change, 4*change, ... and red in between.
    Arriving on red means waiting for the next green, and waiting on green is
    not allowed, so there is exactly one departure time for each arrival.
    """
    if (t // change) % 2:
        return (t // change + 1) * change
    return t


def travel(k: int, cost: int, change: int) -> int:
    """Arrival time after k edges. Every signal is in phase, so this depends only on k."""
    t = 0
    for _ in range(k):
        t = leave(t, change) + cost
    return t


def adjacency(n: int, edges) -> List[List[int]]:
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def two_pop(n: int, edges, strict: bool = True) -> float:
    """BFS that keeps the two smallest distinct edge counts per vertex, each vertex queued at most twice.

    `strict=False` drops the `d1[v] < nd` check, so a second route of the same
    length fills the second slot. That is the version that treats "second" as
    "second route" and not "second value".
    """
    adj = adjacency(n, edges)
    d1 = [INF] * (n + 1)
    d2 = [INF] * (n + 1)
    d1[1] = 0
    queue = deque([(1, 0)])
    while queue:
        u, d = queue.popleft()
        for v in adj[u]:
            nd = d + 1
            if nd < d1[v]:
                d1[v] = nd
                queue.append((v, nd))
            elif (d1[v] < nd or not strict) and nd < d2[v]:
                d2[v] = nd
                queue.append((v, nd))
    return d2[n]


def first_only(n: int, edges) -> float:
    """Ordinary BFS, each vertex settled once, and the second value read off the target's neighbours.

    Only first values ever propagate, so a second value that needs another
    vertex's second value on the way (an odd cycle away from the target) is
    never seen. It can only be too big or missing.
    """
    adj = adjacency(n, edges)
    d1 = [INF] * (n + 1)
    d1[1] = 0
    queue = deque([1])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if d1[v] == INF:
                d1[v] = d1[u] + 1
                queue.append(v)
    later = [d1[u] + 1 for u in adj[n] if d1[u] + 1 > d1[n]]
    return min(later, default=INF)


def time_domain(n: int, edges, cost: int, change: int) -> int:
    """The same two-slot search run on clock times with the signal rule applied at every step.

    No reduction to edge counts, so it checks `travel` and the claim that the
    second time comes from the second count.
    """
    adj = adjacency(n, edges)
    t1 = [INF] * (n + 1)
    t2 = [INF] * (n + 1)
    t1[1] = 0
    heap = [(0, 1)]
    while heap:
        t, u = heapq.heappop(heap)
        nt = leave(t, change) + cost
        for v in adj[u]:
            if nt < t1[v]:
                t1[v] = nt
                heapq.heappush(heap, (nt, v))
            elif t1[v] < nt < t2[v]:
                t2[v] = nt
                heapq.heappush(heap, (nt, v))
    return t2[n]


def simple_only(n: int, edges) -> float:
    """Second smallest length over simple paths. The statement allows revisits, so this can only be too big."""
    adj = adjacency(n, edges)
    lengths = set()
    stack = [(1, 0, 1 << 1)]
    while stack:
        u, d, seen = stack.pop()
        if u == n:
            lengths.add(d)
            continue
        for v in adj[u]:
            if not seen & (1 << v):
                stack.append((v, d + 1, seen | (1 << v)))
    ordered = sorted(lengths)
    return ordered[1] if len(ordered) > 1 else INF


def oracle(n: int, edges) -> Tuple[int, int]:
    """(d1, d2) from the sets of vertices reachable in exactly L steps, L = 0, 1, 2, ...

    No distances are stored and nothing is settled: layer L+1 is the neighbour
    set of layer L, and the answer is the first two L whose layer holds n.
    """
    adj = adjacency(n, edges)
    layer = {1}
    found = []
    for length in range(2 * n + 4):
        if n in layer:
            found.append(length)
            if len(found) == 2:
                return found[0], found[1]
        layer = {v for u in layer for v in adj[u]}
    raise AssertionError("a connected graph with n >= 2 always has a bounce")


def bfs_from(n: int, adj, src: int) -> List[float]:
    dist = [INF] * (n + 1)
    dist[src] = 0
    queue = deque([src])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def bipartite(n: int, adj) -> bool:
    dist = bfs_from(n, adj, 1)
    return all((dist[u] - dist[v]) % 2 for u in range(1, n + 1) for v in adj[u])


def one_more_edge(n: int, edges) -> bool:
    """Is there an edge (u, v) with d(1, u) + d(v, n) == d(1, n)?

    Along any walk of length d1 + 1, i + d(w_i, n) starts at d1, ends at
    d1 + 1 and moves by 0, 1 or 2, so some step moves it by exactly 1, and that
    step is such an edge. So this should be exactly the d2 == d1 + 1 case.
    """
    adj = adjacency(n, edges)
    a, b = bfs_from(n, adj, 1), bfs_from(n, adj, n)
    return any(a[u] + b[v] == a[n] for u, v in edges) or any(a[v] + b[u] == a[n] for u, v in edges)


class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:
        """Second smallest edge count by the two-slot BFS, then the clock. The rest is in `__main__`."""
        return travel(two_pop(n, edges), time, change)


def connected_graphs(n: int):
    pairs = list(itertools.combinations(range(1, n + 1), 2))
    for mask in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if mask >> i & 1]
        if INF not in bfs_from(n, adjacency(n, edges), 1)[1:]:
            yield edges


def random_connected(rng: random.Random, n: int, m: int):
    edges = {(rng.randint(1, v - 1), v) for v in range(2, n + 1)}
    while len(edges) < m:
        u, v = rng.sample(range(1, n + 1), 2)
        edges.add((min(u, v), max(u, v)))
    return [list(e) for e in edges]


if __name__ == "__main__":
    rng = random.Random(2045)
    started = time.time()
    clocks = ((3, 5), (1, 1), (2, 7), (5, 2))

    print("== every connected graph, against the layer oracle ==")
    print("  n   graphs  two-pop  clock  non-strict  first-only (none)  simple-only (none)"
          "   d1+1  non-bip  non-bip d1+2  edge test")
    for n in range(2, 7):
        total = wrong = clock_wrong = loose = first = first_none = simple = simple_none = 0
        plus_one = non_bip = non_bip_two = edge_wrong = 0
        for edges in connected_graphs(n):
            total += 1
            d1, d2 = oracle(n, edges)
            wrong += two_pop(n, edges) != d2
            for cost, change in clocks:
                clock_wrong += time_domain(n, edges, cost, change) != travel(d2, cost, change)
            loose += two_pop(n, edges, strict=False) != d2
            f = first_only(n, edges)
            assert f >= d2
            first += f != d2
            first_none += f == INF
            s = simple_only(n, edges)
            assert s >= d2
            simple += s != d2
            simple_none += s == INF
            plus_one += d2 == d1 + 1
            nb = not bipartite(n, adjacency(n, edges))
            non_bip += nb
            non_bip_two += nb and d2 == d1 + 2
            edge_wrong += one_more_edge(n, edges) != (d2 == d1 + 1)
            assert d2 in (d1 + 1, d1 + 2)
        print(f"  {n}  {total:7d}  {wrong:7d}  {clock_wrong:5d}  {loose:10d}  {first:10d} ({first_none:4d})"
              f"  {simple:11d} ({simple_none:4d})  {plus_one:6d}  {non_bip:7d}  {non_bip_two:12d}  {edge_wrong:9d}")

    print("\n== random graphs, two-pop against the oracle and the clock search ==")
    for n, m, count in ((10, 12, 3000), (30, 40, 1000), (200, 250, 200)):
        wrong = clock_wrong = plus_one = non_bip_two = 0
        for _ in range(count):
            edges = random_connected(rng, n, m)
            d1, d2 = oracle(n, edges)
            wrong += two_pop(n, edges) != d2
            cost, change = rng.randint(1, 1000), rng.randint(1, 1000)
            clock_wrong += time_domain(n, edges, cost, change) != travel(d2, cost, change)
            plus_one += d2 == d1 + 1
            non_bip_two += (not bipartite(n, adjacency(n, edges))) and d2 == d1 + 2
        print(f"  n {n:3d} m {m:3d}  graphs {count}   two-pop wrong {wrong}   clock wrong {clock_wrong}"
              f"   d1+1 {plus_one}   non-bipartite at d1+2 {non_bip_two}")

    print("\n== the statement's size, timed ==")
    s = Solution()
    path = [[v, v + 1] for v in range(1, 10 ** 4)]
    for label, n, edges in (("random m = 2e4", 10 ** 4, random_connected(rng, 10 ** 4, 2 * 10 ** 4)),
                            ("path", 10 ** 4, path),
                            ("path + triangle at 1", 10 ** 4, path + [[1, 3]])):
        t0 = time.time()
        ans = s.secondMinimum(n, edges, 1000, 1000)
        print(f"  {label:22s} answer {ans:10d}   {time.time() - t0:.3f}s")

    print(f"\n{time.time() - started:.0f}s")
