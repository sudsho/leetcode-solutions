import itertools
import random
import time
from collections import deque
from typing import List

H, V = 0, 1
# move kinds, in the order the textbook search tries them
RIGHT, DOWN, CW, CCW = range(4)


def moves(grid, r, c, o, order=(RIGHT, DOWN, CW, CCW)):
    """Successors of the snake with its tail on (r, c) and orientation o, in the given move order.

    Horizontal covers (r, c) and (r, c + 1), vertical (r, c) and (r + 1, c).
    Right and down shift both cells. A rotation keeps the tail and needs the
    whole 2 x 2 block at (r, c) free, the same block in both directions.
    """
    n = len(grid)

    def free(i, j):
        return i < n and j < n and grid[i][j] == 0

    block = free(r + 1, c) and free(r, c + 1) and free(r + 1, c + 1)
    out = []
    for m in order:
        if m == RIGHT:
            if o == H and free(r, c + 2):
                out.append((r, c + 1, H))
            elif o == V and free(r, c + 1) and free(r + 1, c + 1):
                out.append((r, c + 1, V))
        elif m == DOWN:
            if o == H and free(r + 1, c) and free(r + 1, c + 1):
                out.append((r + 1, c, H))
            elif o == V and free(r + 2, c):
                out.append((r + 1, c, V))
        elif m == CW and o == H and block:
            out.append((r, c, V))
        elif m == CCW and o == V and block:
            out.append((r, c, H))
    return out


def head(state):
    r, c, o = state
    return (r, c + 1) if o == H else (r + 1, c)


def bfs(grid, key=lambda s: s, order=(RIGHT, DOWN, CW, CCW), counter=None):
    """BFS from the start, marking key(state) on first arrival. key = identity is the real search."""
    n = len(grid)
    start, goal = (0, 0, H), (n - 1, n - 2, H)
    if grid[0][0] or grid[0][1]:
        return -1
    seen = {key(start)}
    q = deque([(start, 0)])
    while q:
        s, d = q.popleft()
        if counter is not None:
            counter[0] += 1
        if s == goal:
            return d
        for t in moves(grid, *s, order=order):
            k = key(t)
            if k not in seen:
                seen.add(k)
                q.append((t, d + 1))
    return -1


def one_mark_head(grid, order=(RIGHT, DOWN, CW, CCW)):
    """One mark per head cell: the snake with its head on a cell counts once, whichever way it lies."""
    return bfs(grid, head, order)


def one_mark_tail(grid, order=(RIGHT, DOWN, CW, CCW)):
    """One mark per tail cell. A rotation keeps the tail, so this one can never turn at all."""
    return bfs(grid, lambda s: s[:2], order)


def oracle(grid):
    """DP over tail cells in order of r + c, with no queue and no marks.

    Right and down raise r + c by one and a rotation keeps the tail, so a cell's
    two orientations depend only on the cells above and to the left and then on
    each other through the one shared 2 x 2 block.
    """
    n = len(grid)
    inf = float("inf")
    dist = [[[inf, inf] for _ in range(n)] for _ in range(n)]

    def ok(r, c, o):
        r2, c2 = (r, c + 1) if o == H else (r + 1, c)
        return r2 < n and c2 < n and grid[r][c] == 0 and grid[r2][c2] == 0

    for s in range(2 * n - 1):
        for r in range(max(0, s - n + 1), min(n, s + 1)):
            c = s - r
            for o in (H, V):
                if not ok(r, c, o):
                    continue
                if (r, c, o) == (0, 0, H):
                    dist[r][c][o] = 0
                if c > 0 and ok(r, c - 1, o):
                    dist[r][c][o] = min(dist[r][c][o], dist[r][c - 1][o] + 1)
                if r > 0 and ok(r - 1, c, o):
                    dist[r][c][o] = min(dist[r][c][o], dist[r - 1][c][o] + 1)
            if ok(r, c, H) and ok(r, c, V) and r + 1 < n and c + 1 < n and grid[r + 1][c + 1] == 0:
                h, v = dist[r][c]
                dist[r][c] = [min(h, v + 1), min(v, h + 1)]
    d = dist[n - 1][n - 2][H]
    return -1 if d == inf else d


class Solution:
    def minimumMoves(self, grid: List[List[int]]) -> int:
        return bfs(grid)


def all_grids(n):
    """Every n x n grid with the two start cells free."""
    rest = n * n - 2
    for bits in range(1 << rest):
        cells = [0, 0] + [(bits >> i) & 1 for i in range(rest)]
        yield [cells[i * n:(i + 1) * n] for i in range(n)]


def random_grid(rng, n, wall):
    g = [[1 if rng.random() < wall else 0 for _ in range(n)] for _ in range(n)]
    g[0][0] = g[0][1] = 0
    return g


def head_path_self_avoiding(grid):
    """Whether some shortest solution's head never stands on a cell twice, checked by BFS on (state, heads so far)."""
    want = bfs(grid)
    if want < 0:
        return True
    start = (0, 0, H)
    layer = {(start, frozenset([head(start)]))}
    for _ in range(want):
        layer = {(t, hs | {head(t)}) for s, hs in layer for t in moves(grid, *s) if head(t) not in hs}
    n = len(grid)
    return any(s == (n - 1, n - 2, H) for s, _ in layer)


if __name__ == "__main__":
    t0 = time.time()
    s = Solution()
    ex1 = [[0, 0, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0], [0, 0, 0, 0, 1, 1],
           [0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0]]
    ex2 = [[0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1], [1, 1, 0, 0, 0, 1],
           [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], [1, 1, 1, 0, 0, 0]]
    print("examples", s.minimumMoves(ex1), s.minimumMoves(ex2), "want 11 9")

    orders = list(itertools.permutations(range(4)))
    print("\nexhaustive, every grid with the start free, all 24 move orders")
    for n in (3, 4):
        total = off = tail_wrong = solvable = needs_turn = 0
        head_wrong = [0] * len(orders)
        witness = None
        avoid_fail = 0
        for g in all_grids(n):
            total += 1
            want = bfs(g)
            off += oracle(g) != want
            solvable += want >= 0
            got_tail = one_mark_tail(g)
            tail_wrong += got_tail != want
            needs_turn += want >= 0 and got_tail != want
            for i, od in enumerate(orders):
                bad = one_mark_head(g, od) != want
                head_wrong[i] += bad
                if bad and i == 0:
                    avoid_fail += not head_path_self_avoiding(g)
                    if witness is None:
                        witness = g
        print(f"  {n}x{n}: {total} grids, {solvable} solvable, oracle off {off}, "
              f"tail mark wrong {tail_wrong} (all of them need a turn: {tail_wrong == needs_turn}), "
              f"head mark wrong min {min(head_wrong)} max {max(head_wrong)} over orders, "
              f"failures with no head-self-avoiding shortest path {avoid_fail}")
        if witness is not None:
            print(f"    witness {witness}: answer {bfs(witness)}, head mark {one_mark_head(witness)}")

    print("\nrandom, 4000 grids at each size and wall density")
    rng = random.Random(1210)
    for n in (5, 6, 8):
        for wall in (0.0, 0.1, 0.2, 0.3):
            wrong = long = off = solv = 0
            for _ in range(4000):
                g = random_grid(rng, n, wall)
                want = bfs(g)
                solv += want >= 0
                off += oracle(g) != want
                got = one_mark_head(g)
                wrong += got != want
                long += got > want >= 0
            print(f"  {n}x{n} walls {wall:.1f}: solvable {solv}, oracle off {off}, head mark wrong {wrong} "
                  f"({long} too long, {wrong - long} say -1)")

    print("\ntime at 100x100, 50 grids at walls 0.1, pops")
    grids = [random_grid(rng, 100, 0.1) for _ in range(50)]
    for name, fn in (("bfs", bfs), ("oracle", oracle)):
        tt = time.perf_counter()
        for g in grids:
            fn(g)
        print(f"  {name:6s} {1000 * (time.perf_counter() - tt) / len(grids):.2f} ms")

    print(f"\n{time.time() - t0:.0f} s")
