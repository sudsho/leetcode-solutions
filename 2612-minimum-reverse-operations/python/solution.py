import bisect
import itertools
import random
import time
from collections import deque
from typing import List, Tuple


def landing(i: int, n: int, k: int) -> Tuple[int, int]:
    """First and last index a 1 at `i` can land on in one reversal of length k, stride 2.

    Reversing `[left, left + k - 1]` with `i` inside sends it to
    `2 * left + k - 1 - i`, and `left` runs over `max(0, i - k + 1)` to
    `min(i, n - k)`, so the landings are one run of a single parity.
    """
    return 2 * max(0, i - k + 1) + k - 1 - i, 2 * min(i, n - k) + k - 1 - i


def oracle(n: int, p: int, banned: List[int], k: int):
    """Distances and shortest-sequence counts from the reversal itself.

    Every choice of `left` is simulated on an actual array, so neither the
    stride-2 run nor any skip structure is trusted. A sequence is a sequence of
    subarrays, and two subarrays from the same position never land in the same
    place, asserted, so it is also a path in the position graph.
    """
    blocked = set(banned)
    dist = [-1] * n
    ways = [0] * n
    dist[p], ways[p] = 0, 1
    queue = deque([p])
    while queue:
        i = queue.popleft()
        seen = set()
        for left in range(max(0, i - k + 1), min(i, n - k) + 1):
            row = [0] * n
            row[i] = 1
            row[left:left + k] = row[left:left + k][::-1]
            j = row.index(1)
            assert j not in seen
            seen.add(j)
            if j == i or j in blocked:
                continue
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
            if dist[j] == dist[i] + 1:
                ways[j] += ways[i]
    return dist, ways


def find(nxt: List[int], j: int) -> int:
    """Smallest index >= j of j's parity still in the free set, with path halving."""
    root = j
    while nxt[root] != root:
        root = nxt[root]
    while nxt[j] != root:
        nxt[j], j = root, nxt[j]
    return root


def free_set(n: int, p: int, banned: List[int]) -> List[int]:
    nxt = list(range(n + 2))
    for j in set(banned) | {p}:
        nxt[j] = j + 2
    return nxt


def min_ops(n: int, p: int, banned: List[int], k: int, clear: bool = True):
    """BFS over positions with a skip pointer per parity. Returns (answer, indices examined)."""
    nxt = free_set(n, p, banned)
    dist = [-1] * n
    dist[p] = 0
    queue = deque([p])
    scans = 0
    while queue:
        i = queue.popleft()
        lo, hi = landing(i, n, k)
        j = find(nxt, lo)
        while j <= hi:
            scans += 1
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
            else:
                assert not clear
            if clear:
                nxt[j] = j + 2
            j = find(nxt, j + 2)
        scans += 1
    return dist, scans


def count_ops(n: int, p: int, banned: List[int], k: int, clear: bool):
    """`min_ops` with a `+=` for the number of shortest sequences, the clear switchable."""
    nxt = free_set(n, p, banned)
    dist = [-1] * n
    ways = [0] * n
    dist[p], ways[p] = 0, 1
    queue = deque([p])
    while queue:
        i = queue.popleft()
        lo, hi = landing(i, n, k)
        j = find(nxt, lo)
        while j <= hi:
            if dist[j] == -1:
                dist[j] = dist[i] + 1
                queue.append(j)
            if dist[j] == dist[i] + 1:
                ways[j] += ways[i]
            if clear:
                nxt[j] = j + 2
            j = find(nxt, j + 2)
    return dist, ways


def count_by_levels(n: int, p: int, banned: List[int], k: int):
    """Counts with the clear kept, each new position pulling from the finished level.

    Two facts make the pull one range sum. The relation is symmetric, since
    reversing the same subarray again puts the 1 back, so the positions that
    reach `j` are `landing(j)` itself. And a reversal of length k moves the 1 by
    `k - 1 - 2i` mod 2, so every position at one level has the same parity, and
    every level position inside `landing(j)` numerically is a predecessor. Sort
    the level once, prefix-sum its counts, two bisections per new position.
    Returns (dist, ways, positions looked up).
    """
    nxt = free_set(n, p, banned)
    dist = [-1] * n
    ways = [0] * n
    dist[p], ways[p] = 0, 1
    frontier = [p]
    lookups = 0
    while frontier:
        assert len({i % 2 for i in frontier}) == 1
        found = []
        for i in frontier:
            lo, hi = landing(i, n, k)
            j = find(nxt, lo)
            while j <= hi:
                dist[j] = dist[i] + 1
                found.append(j)
                nxt[j] = j + 2
                j = find(nxt, j + 2)
        level = sorted(frontier)
        prefix = [0]
        for i in level:
            prefix.append(prefix[-1] + ways[i])
        for j in found:
            lo, hi = landing(j, n, k)
            ways[j] = prefix[bisect.bisect_right(level, hi)] - prefix[bisect.bisect_left(level, lo)]
            lookups += 1
        frontier = found
    return dist, ways, lookups


class Solution:
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        """BFS on positions, where one reversal moves the 1 anywhere in a stride-2 run.

        The skip pointers hold the unvisited positions of each parity, so every
        position is handed out once and the BFS is O(n alpha(n)) rather than
        O(nk). Whether the skip survives counting, and what replaces it, is run
        in `__main__`.
        """
        return min_ops(n, p, banned, k)[0]


if __name__ == "__main__":
    random.seed(2612)
    started = time.time()

    print("exhaustive: every n <= 9, p, k and banned set not holding p")
    print("  n  instances  reachable-nonstart  >1 sequence   keep+copy wrong(inst)  max dist  max ways")
    by_nk = {}
    for n in range(1, 10):
        instances = reach = multi = wrong_instances = 0
        max_dist = max_ways = 0
        for p in range(n):
            others = [j for j in range(n) if j != p]
            for k in range(1, n + 1):
                for size in range(len(others) + 1):
                    for banned in itertools.combinations(others, size):
                        banned = list(banned)
                        truth_dist, truth_ways = oracle(n, p, banned, k)
                        assert min_ops(n, p, banned, k, clear=True)[0] == truth_dist
                        assert min_ops(n, p, banned, k, clear=False)[0] == truth_dist
                        kept = count_ops(n, p, banned, k, clear=True)
                        dropped = count_ops(n, p, banned, k, clear=False)
                        pulled = count_by_levels(n, p, banned, k)
                        assert dropped == (truth_dist, truth_ways)
                        assert pulled[:2] == (truth_dist, truth_ways)
                        assert kept[0] == truth_dist
                        assert all(kept[1][j] == 1 for j in range(n) if truth_dist[j] >= 0)
                        r = sum(1 for j in range(n) if truth_dist[j] > 0)
                        m = sum(1 for j in range(n) if truth_ways[j] > 1)
                        cell = by_nk.setdefault((n, k), [0, 0])
                        cell[0] += r
                        cell[1] += m
                        instances += 1
                        reach += r
                        multi += m
                        wrong_instances += m > 0
                        max_dist = max(max_dist, max(truth_dist))
                        max_ways = max(max_ways, max(truth_ways))
        print(f"  {n}  {instances:9d}  {reach:18d}  {multi:11d}   {wrong_instances:20d}  {max_dist:8d}  {max_ways:8d}")

    print("\nshare of reachable non-start positions with more than one shortest sequence, by k")
    for n in (8, 9):
        print(f"  n={n}  " + "  ".join(
            f"k={k}:{by_nk[(n, k)][1] / by_nk[(n, k)][0]:.3f}" if by_nk[(n, k)][0] else f"k={k}:-"
            for k in range(1, n + 1)))

    print("\nnecessary: positions examined, no banned, p = 0")
    for n in (1000, 4000):
        for k in (2, 3, 51, n // 2, n - 1):
            dist_kept, kept = min_ops(n, 0, [], k, clear=True)
            dist_dropped, dropped = min_ops(n, 0, [], k, clear=False)
            assert dist_kept == dist_dropped
            reached = sum(1 for x in dist_kept if x >= 0)
            window = 0
            for i in range(n):
                if dist_kept[i] >= 0:
                    lo, hi = landing(i, n, k)
                    # p starts outside the free set, so even without the clear it is skipped.
                    window += (hi - lo) // 2 + 1 - (lo <= 0 <= hi and lo % 2 == 0)
            assert dropped == window + reached and kept == 2 * reached - 1
            print(f"  n={n:5d} k={k:5d}  reachable {reached:5d}  kept {kept:8d}  dropped {dropped:9d}"
                  f"  ratio {dropped / kept:8.2f}  levels {max(dist_kept):5d}")

    print("\nrandom counting, n = 60")
    for k, ban in ((3, 0.0), (3, 0.3), (5, 0.1), (8, 0.1), (9, 0.1), (20, 0.2), (21, 0.2), (45, 0.4)):
        reach = multi = 0
        worst_lookups = 0.0
        biggest = 0
        for _ in range(300):
            p = random.randrange(60)
            banned = [j for j in range(60) if j != p and random.random() < ban]
            truth_dist, truth_ways = oracle(60, p, banned, k)
            dist, ways, lookups = count_by_levels(60, p, banned, k)
            assert (dist, ways) == (truth_dist, truth_ways)
            assert count_ops(60, p, banned, k, clear=False)[1] == truth_ways
            reach += sum(1 for x in truth_dist if x > 0)
            multi += sum(1 for w in truth_ways if w > 1)
            biggest = max(biggest, max(truth_ways))
        print(f"  k={k:2d} banned~{ban:.1f}  reachable non-start {reach:5d}  >1 sequence {multi:5d}"
              f" ({multi / max(reach, 1):.3f})   largest count {biggest}")

    print("\nlarge: pull against the O(nk) += with the clear deleted, p = n // 2, 5% banned")
    for n, k in ((5000, 8), (5000, 101), (5000, 1000), (5000, 2500)):
        p = n // 2
        banned = random.sample([j for j in range(n) if j != p], n // 20)
        t0 = time.time()
        dist, ways, lookups = count_by_levels(n, p, banned, k)
        t_pull = time.time() - t0
        t0 = time.time()
        assert count_ops(n, p, banned, k, clear=False) == (dist, ways)
        t_push = time.time() - t0
        reached = sum(1 for x in dist if x >= 0)
        print(f"  n={n} k={k:5d}  reachable {reached:5d}  levels {max(dist):4d}  pull {t_pull:6.3f}s"
              f"  delete+add {t_push:6.3f}s  largest count has {len(str(max(ways)))} digits")
    print(f"\n{time.time() - started:.0f}s")
