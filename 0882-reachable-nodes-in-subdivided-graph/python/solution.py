import heapq
import itertools
import random
from collections import deque
from typing import Dict, List, Tuple


def oracle_reachable(edges: List[List[int]], max_moves: int, n: int) -> int:
    """Reachable count by building the subdivided graph and walking it.

    Every edge `[u, v, cnt]` becomes a path of `cnt + 1` unit edges through `cnt`
    fresh nodes, and a plain BFS counts what lies within `max_moves`. No heap,
    no per-edge bookkeeping, nothing in it can be popped twice.
    """
    adjacent: List[List[int]] = [[] for _ in range(n)]
    for u, v, cnt in edges:
        prev = u
        for _ in range(cnt):
            adjacent.append([])
            node = len(adjacent) - 1
            adjacent[prev].append(node)
            adjacent[node].append(prev)
            prev = node
        adjacent[prev].append(v)
        adjacent[v].append(prev)

    dist = [-1] * len(adjacent)
    dist[0] = 0
    queue = deque([0])
    while queue:
        x = queue.popleft()
        if dist[x] == max_moves:
            continue
        for y in adjacent[x]:
            if dist[y] < 0:
                dist[y] = dist[x] + 1
                queue.append(y)
    return sum(1 for d in dist if d >= 0)


def reach(
    edges: List[List[int]],
    max_moves: int,
    n: int,
    skip_stale: bool = True,
    read_key: bool = True,
    overwrite: bool = True,
    count_pops: bool = True,
) -> Tuple[int, int]:
    """The textbook program, instrumented, with four switches exposed.

    Returns `(answer, stale_pops)`. `skip_stale` is `if d > dist[u]: continue`.
    `read_key` picks what the pop reads, `d` or `dist[u]`. `overwrite` picks the
    edge update, `used[u, v] = walk` or `used[u, v] = max(used[u, v], walk)`.
    `count_pops` picks where the original nodes are counted, `answer += 1` on
    every pop that gets past the guard or `dist[x] <= max_moves` at the end.

    With the guard in place every node reaches the loop once and with
    `d == dist[u]`, so the last three switches are invisible and all eight
    guarded programs are the same function.
    """
    adjacent: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, cnt in edges:
        adjacent[u].append((v, cnt))
        adjacent[v].append((u, cnt))

    dist = [float("inf")] * n
    dist[0] = 0
    heap = [(0, 0)]
    used: Dict[Tuple[int, int], int] = {}
    answer = stale = 0
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            stale += 1
            if skip_stale:
                continue
        if count_pops:
            answer += 1
        base = d if read_key else dist[u]
        for v, cnt in adjacent[u]:
            walk = min(cnt, max_moves - base)
            used[u, v] = walk if overwrite else max(used.get((u, v), 0), walk)
            candidate = base + cnt + 1
            if candidate <= max_moves and candidate < dist[v]:
                dist[v] = candidate
                heapq.heappush(heap, (candidate, v))

    if not count_pops:
        answer = sum(1 for x in dist if x <= max_moves)
    for u, v, cnt in edges:
        answer += min(cnt, used.get((u, v), 0) + used.get((v, u), 0))
    return answer, stale


class Solution:
    def reachableNodes(self, edges: List[List[int]], maxMoves: int, n: int) -> int:
        """Nodes of the subdivided graph within `maxMoves` of node 0.

        Picked as the check the 10th's rule asks for. That night the stale-entry
        skip in counting Dijkstra was harmless if the relaxation read the popped
        key `d` and a wrong answer if it read `dist[u]`, and I filed the property
        under the guard together with the read it hides. That is a claim about
        which read is safe, and any Dijkstra whose pop feeds something other
        than the relaxation can test it.

        This one feeds two. The textbook program - this one, line for line -
        counts an original node with `answer += 1` on every pop the guard lets
        through, and records how far the budget reaches into each edge with
        `used[u, v] = min(cnt, maxMoves - d)`, an overwrite that reads the key.
        With the guard both happen once per node at `d == dist[u]`, so the read,
        the edge update and where the count is taken are all free. Sixteen
        programs, and the eight that keep the guard agree with a BFS on the
        subdivided graph on every instance in `__main__`.

        Without it, over every graph on 4 nodes with counts up to 2 and budgets
        up to 8, and on 5 nodes with counts up to 1:

        - the counter is wrong on every instance with a stale pop, 2916 of 2916
          and 7218 of 7218, under either read, because it reads nothing;
        - the overwrite reading `d` is wrong on 120 and 324. A stale pop comes
          after the real one and writes a shorter reach over it;
        - the overwrite reading `dist[u]` is wrong on none. It writes the same
          value again;
        - a max is wrong on none under either read.

        So the read 1976 found safe is the one that breaks here, and the one it
        found harmful is fine. Neither read is the property. What fits both
        nights is per update: whether it absorbs a repeat under the value the
        read hands it. A strict `<` absorbs both reads, a max absorbs both, an
        overwrite absorbs only an identical value, and `+=` absorbs nothing -
        1976's `==` branch was only safe from `d` because a strictly larger
        offer never reaches it.

        The two bugs in the textbook program also cancel. Minus its guard it is
        right on 117 and 288 of the stale instances, and in every one of them
        the overwrite undercounts by exactly the number of stale pops the
        counter adds back.

        Kept as the textbook has it: guard, `d`, overwrite, counter. The last
        three are each safe only because of the first.
        """
        adjacent: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        for u, v, cnt in edges:
            adjacent[u].append((v, cnt))
            adjacent[v].append((u, cnt))

        dist = [float("inf")] * n
        dist[0] = 0
        heap = [(0, 0)]
        used: Dict[Tuple[int, int], int] = {}
        answer = 0
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            answer += 1
            for v, cnt in adjacent[u]:
                used[u, v] = min(cnt, maxMoves - d)
                candidate = d + cnt + 1
                if candidate <= maxMoves and candidate < dist[v]:
                    dist[v] = candidate
                    heapq.heappush(heap, (candidate, v))

        for u, v, cnt in edges:
            answer += min(cnt, used.get((u, v), 0) + used.get((v, u), 0))
        return answer


def all_graphs(n: int, counts: Tuple[int, ...]):
    """Every graph on n labelled nodes with each pair absent or subdivided by
    one of `counts`."""
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product((None,) + counts, repeat=len(pairs)):
        yield [[u, v, c] for (u, v), c in zip(pairs, choice) if c is not None]


def lasso(length: int, max_moves: int) -> List[List[int]]:
    """Four nodes. `0 - 2` directly at weight `length`, `0 - 1 - 2` at weight 2,
    and a pendant `2 - 3` subdivided `max_moves` times so it never saturates.

    Node 2 is pushed at `length` first, improved to 2, popped for real at 2 and
    then popped again, stale, at `length`.
    """
    return [[0, 2, length - 1], [0, 1, 0], [1, 2, 0], [2, 3, max_moves]]


VARIANTS = {
    (read_key, overwrite, count_pops): (
        f"{'d      ' if read_key else 'dist[u]'}  "
        f"{'overwrite' if overwrite else 'max      '}  "
        f"{'per pop' if count_pops else 'at end '}"
    )
    for read_key, overwrite, count_pops in itertools.product((True, False), repeat=3)
}


if __name__ == "__main__":
    import time

    t0 = time.time()
    solution = Solution()

    cases = [
        ([[0, 1, 10], [0, 2, 1], [1, 2, 2]], 6, 3, 13),
        ([[0, 1, 4], [1, 2, 6], [0, 2, 8], [1, 3, 1]], 10, 4, 23),
        ([[1, 2, 4], [1, 4, 5], [1, 3, 1], [2, 3, 4], [3, 4, 5]], 17, 5, 1),
        ([], 0, 1, 1),
        ([[0, 1, 0]], 0, 2, 1),
    ]
    print("answers")
    for edges, moves, n, expected in cases:
        got = solution.reachableNodes(edges, moves, n)
        assert got == expected == oracle_reachable(edges, moves, n), (edges, got, expected)
        print(f"  n={n}  maxMoves={moves:2d}  reachable={got}")

    # written before the run. the 10th's rule was that dropping the guard is
    # harmless when the pop reads d and a wrong answer when it reads dist[u]. two
    # updates here that 1976 did not have, and my prediction for each:
    #   - the per-pop counter is wrong on every instance with an in-range stale
    #     pop, whichever quantity is read, because it reads neither.
    #   - the overwrite reading d is the one the 10th's rule calls safe and i
    #     expect it to be wrong, but rarely: a stale pop can only lower used[u, v]
    #     where max_moves - d < cnt, and min(cnt, sum of both sides) saturates on
    #     most edges anyway. so far fewer wrong than the counter, and falling as
    #     max_moves grows, since a longer budget saturates more edges from the
    #     far side.
    # the first is right. the second is right on the exhaustive sets, about 4%,
    # and wrong where it matters: on random 30-node graphs it is wrong on 278 of
    # the 279 with a stale pop at budget 10. it does fall with the budget, but as
    # a cliff - 278, 54, 0 at 10, 20, 40 - and the small graphs only looked safe
    # because at counts up to 2 nearly every edge is saturated already.
    print("\nall sixteen programs against the oracle, exhaustively")
    for n, counts, budgets in ((4, (0, 1, 2), range(0, 9)), (5, (0, 1), (2, 3, 4))):
        instances = with_stale = cancelled = 0
        wrong = {key: 0 for key in VARIANTS}
        for edges in all_graphs(n, counts):
            for moves in budgets:
                truth = oracle_reachable(edges, moves, n)
                instances += 1
                got_by_key = {}
                for key in VARIANTS:
                    guarded, _ = reach(edges, moves, n, True, *key)
                    assert guarded == truth, (edges, moves, key)
                    got, stale = reach(edges, moves, n, False, *key)
                    wrong[key] += got != truth
                    got_by_key[key] = got
                with_stale += stale > 0
                # the textbook program minus its guard, right only because its
                # two errors cancel: the counter's +stale against the overwrite's
                if stale > 0 and got_by_key[True, True, True] == truth:
                    assert got_by_key[True, True, False] - truth == -stale, (edges, moves)
                    cancelled += 1
        print(f"  n={n} counts={counts} budgets={list(budgets)}")
        print(f"    {instances} instances, {with_stale} with an in-range stale pop, "
              f"every guarded program right on all of them")
        print("    unguarded:  read     update     count     wrong")
        for key, label in VARIANTS.items():
            print(f"                {label}  {wrong[key]:6d}")
        print(f"    textbook minus the guard right on {cancelled} stale instances, every one of"
              f" them the overwrite undercounting by exactly the number of stale pops")

    print("\nthe lasso, where the overwrite reading d is wrong by construction")
    print("  error against the oracle with the guard removed")
    for length in (3, 5, 10, 50):
        moves = length + 5
        edges = lasso(length, moves)
        truth = oracle_reachable(edges, moves, 4)
        over_d, stale = reach(edges, moves, 4, False, True, True, False)
        over_dist, _ = reach(edges, moves, 4, False, False, True, False)
        counter, _ = reach(edges, moves, 4, False, False, False, True)
        textbook, _ = reach(edges, moves, 4, False, True, True, True)
        assert over_d - truth == 2 - length and over_dist == truth and counter - truth == stale == 1
        print(f"  length={length:3d}  maxMoves={moves:3d}  truth={truth:4d}  stale pops={stale}"
              f"   overwrite from d {over_d - truth:+4d}   from dist[u] {over_dist - truth:+d}"
              f"   counter {counter - truth:+d}   textbook, both {textbook - truth:+4d}")

    print("\nrandom graphs, n=30, edge prob 0.25, cnt in [0, 10], 300 per budget")
    rng = random.Random(882)
    for moves in (2, 5, 10, 20, 40, 80, 200):
        stale_graphs = counter_wrong = overwrite_wrong = textbook_wrong = 0
        for _ in range(300):
            n = 30
            edges = [[u, v, rng.randint(0, 10)] for u, v in itertools.combinations(range(n), 2)
                     if rng.random() < 0.25]
            truth, _ = reach(edges, moves, n)
            got_counter, stale = reach(edges, moves, n, False, False, False, True)
            got_overwrite, _ = reach(edges, moves, n, False, True, True, False)
            got_textbook, _ = reach(edges, moves, n, False)
            stale_graphs += stale > 0
            counter_wrong += got_counter != truth
            overwrite_wrong += got_overwrite != truth
            textbook_wrong += got_textbook != truth
        print(f"  maxMoves={moves:4d}  stale pops in {stale_graphs:3d}/300"
              f"   counter wrong {counter_wrong:3d}   overwrite-from-d wrong {overwrite_wrong:3d}"
              f"   textbook minus guard wrong {textbook_wrong:3d}")

    print(f"\ndone in {time.time() - t0:.1f}s")
