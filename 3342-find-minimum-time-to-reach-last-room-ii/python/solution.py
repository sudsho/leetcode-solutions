import heapq
import itertools
import random
import time
from typing import List

INF = float("inf")

GRID = ((1, 0), (-1, 0), (0, 1), (0, -1))
KING = GRID + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def step_cost(k: int, first: int = 1) -> int:
    """Cost of move number k (0-based). Moves alternate 1, 2, 1, 2, ... from `first`."""
    return first if k % 2 == 0 else 3 - first


def arrive(t: int, gate: int, k: int, first: int = 1, as_arrival: bool = False) -> int:
    """Arrival time in a room with moveTime `gate`, leaving the last room no earlier than t, as move number k.

    The statement's gate is on the start of the move: wait until max(t, gate),
    then walk. `as_arrival=True` reads it as a bound on arriving instead,
    max(t + cost, gate), which is never later and is the wrong reading.
    """
    if as_arrival:
        return max(t + step_cost(k, first), gate)
    return max(t, gate) + step_cost(k, first)


def dijkstra(grid, moves=GRID, keep_parity=False, first=1, as_arrival=False) -> float:
    """Dijkstra on the time of arrival.

    The state is the cell, or (cell, parity of the move count) with
    `keep_parity`. The next move's cost depends on the parity, so the cell
    alone is only enough if every walk into a cell has the same parity, which
    is what a 4-neighbour grid being bipartite gives and a king's grid does
    not. With the parity kept, an arrival at a cell is only compared with
    arrivals that pay the same next step, and the arrival function is
    non-decreasing in t, so the settle argument goes through unchanged.
    """
    r, c = len(grid), len(grid[0])
    best = {}
    start = (0, 0, 0)
    best[start] = 0
    heap = [(0, 0, 0, 0)]
    while heap:
        t, i, j, k = heapq.heappop(heap)
        key = (i, j, k % 2 if keep_parity else 0)
        if t > best.get(key, INF):
            continue
        if (i, j) == (r - 1, c - 1):
            return t
        for di, dj in moves:
            a, b = i + di, j + dj
            if 0 <= a < r and 0 <= b < c:
                nt = arrive(t, grid[a][b], k, first, as_arrival)
                nkey = (a, b, (k + 1) % 2 if keep_parity else 0)
                if nt < best.get(nkey, INF):
                    best[nkey] = nt
                    heapq.heappush(heap, (nt, a, b, k + 1))
    return INF


def oracle(grid, moves=GRID, first=1) -> int:
    """Earliest arrival over walks of exactly L moves, for L = 0, 1, 2, ..., nothing settled.

    at[L][cell] is the earliest time some walk of exactly L moves ends in cell.
    `arrive` is non-decreasing in t, so the earliest arrival after L + 1 moves
    comes from the earliest after L, and the recurrence is exact. A walk longer
    than 2 * cells + 2 moves repeats a (cell, parity) pair, and cutting the loop
    out never makes it later, so the answer is the minimum over L up to there.
    """
    r, c = len(grid), len(grid[0])
    cur = {(0, 0): 0}
    ans = cur.get((r - 1, c - 1), INF)
    for k in range(2 * r * c + 2):
        nxt = {}
        for (i, j), t in cur.items():
            for di, dj in moves:
                a, b = i + di, j + dj
                if 0 <= a < r and 0 <= b < c:
                    nt = arrive(t, grid[a][b], k, first)
                    if nt < nxt.get((a, b), INF):
                        nxt[(a, b)] = nt
        cur = nxt
        ans = min(ans, cur.get((r - 1, c - 1), INF))
    return ans


def monotone(grid, first=1) -> int:
    """Right and down moves only. Every such walk has r + c - 2 moves, so the costs are fixed and only the waits vary."""
    r, c = len(grid), len(grid[0])
    at = [[INF] * c for _ in range(r)]
    at[0][0] = 0
    for i in range(r):
        for j in range(c):
            if i or j:
                k = i + j - 1
                prev = min(at[i - 1][j] if i else INF, at[i][j - 1] if j else INF)
                at[i][j] = arrive(prev, grid[i][j], k, first)
    return at[r - 1][c - 1]


class Solution:
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        """Dijkstra on the cell alone, since the grid fixes the parity of every walk into a cell. The rest is in `__main__`."""
        return dijkstra(moveTime)


def grids(r: int, c: int, top: int):
    for rest in itertools.product(range(top + 1), repeat=r * c - 1):
        vals = (0,) + rest
        yield [list(vals[i * c:(i + 1) * c]) for i in range(r)]


if __name__ == "__main__":
    rng = random.Random(3342)
    started = time.time()

    print("== every grid with moveTime[0][0] = 0, against the walk-length oracle ==")
    print("  shape  top   grids  cell  parity  king cell  king parity  as-arrival  first 2  monotone  waits")
    for r, c, top in ((1, 2, 6), (2, 2, 6), (2, 3, 5), (3, 3, 3)):
        total = cell = parity = king_cell = king_parity = arr = first2 = mono = waits = 0
        for g in grids(r, c, top):
            total += 1
            want = oracle(g)
            cell += dijkstra(g) != want
            parity += dijkstra(g, keep_parity=True) != want
            kw = oracle(g, KING)
            king_cell += dijkstra(g, KING) != kw
            king_parity += dijkstra(g, KING, keep_parity=True) != kw
            wa = dijkstra(g, as_arrival=True)
            assert wa <= want
            arr += wa != want
            first2 += oracle(g, first=2) != want
            m = monotone(g)
            assert m >= want
            mono += m != want
            waits += want != (r + c - 2) // 2 * 3 + (r + c - 2) % 2
        print(f"  {r}x{c}    {top}  {total:6d}  {cell:4d}  {parity:6d}  {king_cell:9d}  {king_parity:11d}"
              f"  {arr:10d}  {first2:7d}  {mono:8d}  {waits:5d}")

    print("\n== random grids, larger ==")
    for r, c, top, count in ((4, 4, 20, 2000), (6, 6, 40, 500), (10, 10, 100, 100)):
        cell = king_cell = king_parity = mono = 0
        for _ in range(count):
            g = [[rng.randint(0, top) for _ in range(c)] for _ in range(r)]
            g[0][0] = 0
            want = oracle(g)
            cell += dijkstra(g) != want
            kw = oracle(g, KING)
            king_cell += dijkstra(g, KING) != kw
            king_parity += dijkstra(g, KING, keep_parity=True) != kw
            mono += monotone(g) != want
        print(f"  {r}x{c} top {top:3d}  grids {count}   cell wrong {cell}   king cell wrong {king_cell}"
              f"   king parity wrong {king_parity}   monotone wrong {mono}")

    print("\n== the statement's size, timed ==")
    s = Solution()
    for label, g in (("zeros 750x750", [[0] * 750 for _ in range(750)]),
                     ("random to 1e9", [[rng.randint(0, 10 ** 9) for _ in range(750)] for _ in range(750)])):
        g[0][0] = 0
        t0 = time.time()
        ans = s.minTimeToReach(g)
        print(f"  {label:16s} answer {ans:12d}   {time.time() - t0:.2f}s")

    print(f"\n{time.time() - started:.0f}s")
