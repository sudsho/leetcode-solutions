import heapq
import random
import time
from collections import defaultdict
from typing import Dict, List, Tuple

STEPS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbours(r: int, c: int, m: int, n: int):
    for dr, dc in STEPS:
        i, j = r + dr, c + dc
        if 0 <= i < m and 0 <= j < n:
            yield i, j


def arrival(t: int, value: int) -> int:
    """Earliest time in a cell of value `value` for someone standing next to it at time `t`.

    A move costs 1, so the first candidate is `t + 1`. If the cell is not open
    yet, the wait is spent stepping away and back, two seconds at a time, so the
    arrival keeps the parity of `t + 1` and is the first time at or after
    `value` with that parity.
    """
    step = t + 1
    if value <= step:
        return step
    return value + ((value - step) & 1)


def can_leave_start(grid: List[List[int]]) -> bool:
    """Whether the first move exists at all.

    Everywhere else the wait is free: a cell entered at time `t` was entered
    from a cell of value at most `t - 1`, which is open again at `t + 1`, so
    there is always somewhere to bounce. The start has no cell behind it, so if
    both of its neighbours are shut at time 1 nothing ever moves.
    """
    m, n = len(grid), len(grid[0])
    return any(grid[i][j] <= 1 for i, j in neighbours(0, 0, m, n))


def oracle(grid: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    """Times and counts taken from the moves themselves, with no arrival rule.

    A walk is a sequence of single steps, each into a cell that is open at the
    second it is entered, so bouncing is spelled out rather than folded into a
    closed form. The first second a cell appears is its answer, and the walks
    standing on it at that second are its count.
    """
    m, n = len(grid), len(grid[0])
    horizon = max(max(row) for row in grid) + 2 * m * n + 4
    best = [[-1] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    best[0][0], ways[0][0] = 0, 1
    layer = {(0, 0): 1}
    for t in range(1, horizon + 1):
        nxt: Dict[Tuple[int, int], int] = defaultdict(int)
        for (r, c), w in layer.items():
            for i, j in neighbours(r, c, m, n):
                if grid[i][j] <= t:
                    nxt[(i, j)] += w
        if not nxt:
            break
        for (i, j), w in nxt.items():
            if best[i][j] == -1:
                best[i][j], ways[i][j] = t, w
        layer = nxt
    return best, ways


def push_marked(grid: List[List[int]]):
    """Dijkstra that marks a cell the moment it is pushed, the BFS habit.

    Returns (times, pushes, pops). Each cell enters the heap once and its time
    is written by whoever reaches it first, so there are no stale entries to
    skip.
    """
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    best[0][0] = 0
    if not can_leave_start(grid):
        return best, 0, 0
    seen = [[False] * n for _ in range(m)]
    seen[0][0] = True
    heap = [(0, 0, 0)]
    pushes = pops = 0
    while heap:
        t, r, c = heapq.heappop(heap)
        pops += 1
        for i, j in neighbours(r, c, m, n):
            if seen[i][j]:
                continue
            seen[i][j] = True
            best[i][j] = arrival(t, grid[i][j])
            heapq.heappush(heap, (best[i][j], i, j))
            pushes += 1
    return best, pushes, pops


def pop_settled(grid: List[List[int]]):
    """Dijkstra that settles a cell when it is popped, with stale entries skipped.

    Returns (times, pushes, pops).
    """
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    best[0][0] = 0
    if not can_leave_start(grid):
        return best, 0, 0
    done = [[False] * n for _ in range(m)]
    heap = [(0, 0, 0)]
    pushes = pops = 0
    while heap:
        t, r, c = heapq.heappop(heap)
        pops += 1
        if done[r][c]:
            continue
        done[r][c] = True
        for i, j in neighbours(r, c, m, n):
            if done[i][j]:
                continue
            a = arrival(t, grid[i][j])
            if best[i][j] == -1 or a < best[i][j]:
                best[i][j] = a
                heapq.heappush(heap, (a, i, j))
                pushes += 1
    return best, pushes, pops


def count_push_marked(grid: List[List[int]]):
    """`push_marked` with a count carried along the push.

    A cell is written once, by its first discoverer, so its count is that one
    cell's count. This is the copy that 1871, 1345, 3552 and 2612 all failed on.
    """
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    best[0][0], ways[0][0] = 0, 1
    if not can_leave_start(grid):
        return best, ways
    seen = [[False] * n for _ in range(m)]
    seen[0][0] = True
    heap = [(0, 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        for i, j in neighbours(r, c, m, n):
            if seen[i][j]:
                continue
            seen[i][j] = True
            best[i][j] = arrival(t, grid[i][j])
            ways[i][j] = ways[r][c]
            heapq.heappush(heap, (best[i][j], i, j))
    return best, ways


def count_relax(grid: List[List[int]], reset: bool = True):
    """`pop_settled` with `+=` on a tie and the count reset when the time improves.

    With `reset=False` the improved time keeps the counts the worse time had
    collected, which is the reset every textbook write-up puts in and nothing
    here forces.
    """
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    best[0][0], ways[0][0] = 0, 1
    if not can_leave_start(grid):
        return best, ways
    done = [[False] * n for _ in range(m)]
    heap = [(0, 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if done[r][c]:
            continue
        done[r][c] = True
        for i, j in neighbours(r, c, m, n):
            if done[i][j]:
                continue
            a = arrival(t, grid[i][j])
            if best[i][j] == -1 or a < best[i][j]:
                best[i][j] = a
                ways[i][j] = ways[r][c] if reset else ways[i][j] + ways[r][c]
                heapq.heappush(heap, (a, i, j))
            elif a == best[i][j]:
                ways[i][j] += ways[r][c]
    return best, ways


def count_by_pull(grid: List[List[int]]):
    """`pop_settled` with each cell pulling its count when it is popped.

    Returns (times, ways, predecessor slots examined). The pull is over the four
    neighbours: a settled one whose arrival lands exactly on this cell's time is
    a predecessor, and there is nothing else to filter, since a neighbour that
    is not settled yet cannot become one.
    """
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    ways = [[0] * n for _ in range(m)]
    best[0][0], ways[0][0] = 0, 1
    if not can_leave_start(grid):
        return best, ways, 0
    done = [[False] * n for _ in range(m)]
    heap = [(0, 0, 0)]
    slots = 0
    while heap:
        t, r, c = heapq.heappop(heap)
        if done[r][c]:
            continue
        done[r][c] = True
        if (r, c) != (0, 0):
            total = 0
            for i, j in neighbours(r, c, m, n):
                slots += 1
                if done[i][j] and arrival(best[i][j], grid[r][c]) == t:
                    total += ways[i][j]
            ways[r][c] = total
        for i, j in neighbours(r, c, m, n):
            if done[i][j]:
                continue
            a = arrival(t, grid[i][j])
            if best[i][j] == -1 or a < best[i][j]:
                best[i][j] = a
                heapq.heappush(heap, (a, i, j))
    return best, ways, slots


def waits(grid: List[List[int]], best: List[List[int]]) -> int:
    """Cells whose best time is later than a step from their earliest neighbour."""
    m, n = len(grid), len(grid[0])
    count = 0
    for r in range(m):
        for c in range(n):
            if best[r][c] <= 0:
                continue
            earlier = [best[i][j] for i, j in neighbours(r, c, m, n)
                       if 0 <= best[i][j] < best[r][c]]
            if earlier and best[r][c] > min(earlier) + 1:
                count += 1
    return count


class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        """Dijkstra where the wait to enter a shut cell is a closed form.

        Every path into a cell has the same parity, so a wait rounds up to the
        first second at or past the cell's value with that parity, and no state
        has to carry the parity. Which cell-marking rule survives counting, and
        what the count is a count of, is run in `__main__`.
        """
        m, n = len(grid), len(grid[0])
        return pop_settled(grid)[0][m - 1][n - 1]


def grids(m: int, n: int, top: int):
    """Every m x n grid with grid[0][0] = 0 and the rest in 1..top."""
    cells = m * n - 1
    for code in range(top ** cells):
        flat = [0]
        rest = code
        for _ in range(cells):
            flat.append(rest % top + 1)
            rest //= top
        yield [flat[r * n:(r + 1) * n] for r in range(m)]


def random_grid(m: int, n: int, top: int, rng: random.Random):
    """Values in 1..top with the corner at 0 and one neighbour open at second 1.

    Without the open neighbour almost every grid over a wide range of values is
    the dead one, since both cells next to the corner have to be at most 1, and
    a table of `-1` measures nothing.
    """
    grid = [[rng.randint(1, top) for _ in range(n)] for _ in range(m)]
    grid[0][0] = 0
    if n > 1:
        grid[0][1] = 1
    else:
        grid[1][0] = 1
    return grid


def improvements(grid: List[List[int]]) -> int:
    """Times a tentative time is written twice, which is what the reset is for."""
    m, n = len(grid), len(grid[0])
    best = [[-1] * n for _ in range(m)]
    best[0][0] = 0
    if not can_leave_start(grid):
        return 0
    done = [[False] * n for _ in range(m)]
    heap = [(0, 0, 0)]
    rewrites = 0
    while heap:
        t, r, c = heapq.heappop(heap)
        if done[r][c]:
            continue
        done[r][c] = True
        for i, j in neighbours(r, c, m, n):
            if done[i][j]:
                continue
            a = arrival(t, grid[i][j])
            if best[i][j] == -1:
                best[i][j] = a
                heapq.heappush(heap, (a, i, j))
            elif a < best[i][j]:
                best[i][j] = a
                rewrites += 1
                heapq.heappush(heap, (a, i, j))
    return rewrites


if __name__ == "__main__":
    rng = random.Random(2577)
    started = time.time()

    print("exhaustive: every grid with grid[0][0] = 0 and the rest in 1..top")
    print("  shape  top  grids  reachable  waiting cells  push-mark times wrong"
          "  push-mark counts wrong  no-reset counts wrong  pull wrong")
    parity_checked = agree = disagree = 0
    walk_over = rewrites = wait_grids = 0
    biggest_ratio = (0.0, None)
    for m, n, top in ((2, 2, 4), (2, 3, 4), (3, 3, 3), (2, 4, 3), (1, 5, 4)):
        total = reach = waiting = 0
        bad_pm_time = bad_pm_count = bad_noreset = bad_pull = 0
        for grid in grids(m, n, top):
            truth_best, truth_ways = oracle(grid)
            pm_best, _, _ = push_marked(grid)
            ps_best, _, _ = pop_settled(grid)
            pm_count = count_push_marked(grid)
            reset_count = count_relax(grid, reset=True)
            noreset_count = count_relax(grid, reset=False)
            pull_best, pull_ways, _ = count_by_pull(grid)

            assert ps_best == truth_best
            assert reset_count[0] == truth_best
            assert pull_best == truth_best
            bad_pm_time += pm_best != truth_best

            # every time in a cell has the parity of its distance from the corner.
            for r in range(m):
                for c in range(n):
                    if truth_best[r][c] >= 0:
                        assert truth_best[r][c] % 2 == (r + c) % 2
                        parity_checked += 1

            # the count the arrival rule reports, against the count of walks.
            same = pull_ways == truth_ways
            agree += same
            disagree += not same
            waited = waits(grid, truth_best) > 0
            wait_grids += waited
            assert same or waited, "a grid that never waits still counts differently"
            for r in range(m):
                for c in range(n):
                    if truth_ways[r][c] and pull_ways[r][c]:
                        assert truth_ways[r][c] >= pull_ways[r][c]
                        ratio = truth_ways[r][c] / pull_ways[r][c]
                        if ratio > biggest_ratio[0]:
                            biggest_ratio = (ratio, (m, n, top, r, c))
            walk_over += any(truth_ways[r][c] > pull_ways[r][c]
                             for r in range(m) for c in range(n))

            assert reset_count[1] == pull_ways
            bad_pm_count += pm_count[1] != pull_ways
            bad_noreset += noreset_count[1] != pull_ways
            rewrites += improvements(grid)

            total += 1
            reach += sum(1 for r in range(m) for c in range(n) if truth_best[r][c] > 0)
            waiting += waits(grid, truth_best)
        print(f"  {m}x{n}  {top:3d}  {total:5d}  {reach:9d}  {waiting:13d}"
              f"  {bad_pm_time:21d}  {bad_pm_count:22d}  {bad_noreset:21d}  {bad_pull:10d}")

    print(f"\n  parity of the time against the parity of the cell: {parity_checked} cells, no exception")
    print(f"  tentative times ever written a second time, which is what the reset guards: {rewrites}")
    print(f"  grids where the pull's count equals the walk count: {agree}, differs: {disagree}")
    print(f"  grids holding at least one waiting cell: {wait_grids}, and a grid that never waits never differs")
    print(f"  grids with at least one cell where walks outnumber routes: {walk_over}")
    print(f"  largest walks-to-routes ratio: {biggest_ratio[0]:.1f} at shape/top/cell {biggest_ratio[1]}")

    print("\nrandom grids, counts against the oracle")
    print("  shape  top  grids  waiting cells  push-mark counts wrong  rewrites  routes > 1  max routes digits")
    for m, n, top in ((4, 4, 6), (4, 4, 20), (5, 4, 3), (5, 5, 12), (6, 6, 30)):
        waiting = bad_pm = multi = rewrote = 0
        digits = 0
        for _ in range(400):
            grid = random_grid(m, n, top, rng)
            truth_best, truth_ways = oracle(grid)
            pull_best, pull_ways, _ = count_by_pull(grid)
            assert pull_best == truth_best
            assert push_marked(grid)[0] == truth_best
            assert count_relax(grid, reset=True)[1] == pull_ways
            bad_pm += count_push_marked(grid)[1] != pull_ways
            rewrote += improvements(grid)
            waiting += waits(grid, truth_best)
            multi += sum(1 for r in range(m) for c in range(n) if pull_ways[r][c] > 1)
            digits = max(digits, max(len(str(pull_ways[r][c])) for r in range(m) for c in range(n)))
        print(f"  {m}x{n}  {top:3d}  {400:5d}  {waiting:13d}  {bad_pm:22d}  {rewrote:8d}"
              f"  {multi:10d}  {digits:18d}")

    print("\nthe two marking rules on large grids, times identical, work is not")
    print("  shape       top  pushes(mark)  pushes(settle)  pops(mark)  pops(settle)"
          "  mark  settle  answer")
    for m, n, top in ((300, 300, 10), (300, 300, 10 ** 5), (1000, 1000, 10),
                      (1000, 1000, 10 ** 5), (1000, 1000, 10 ** 9)):
        grid = random_grid(m, n, top, rng)
        t0 = time.time()
        pm_best, pm_push, pm_pop = push_marked(grid)
        t1 = time.time()
        ps_best, ps_push, ps_pop = pop_settled(grid)
        t2 = time.time()
        assert pm_best == ps_best
        print(f"  {m}x{n}  {top:9d}  {pm_push:12d}  {ps_push:14d}  {pm_pop:10d}  {ps_pop:12d}"
              f"  {t1 - t0:5.2f}s  {t2 - t1:6.2f}s  {ps_best[m - 1][n - 1]:6d}")

    print("\nthe pull on large grids, slots examined against cells")
    print("  shape       top  cells  slots  ratio  seconds  largest route count digits")
    for m, n, top in ((300, 300, 10), (300, 300, 10 ** 5), (600, 600, 10 ** 5)):
        grid = random_grid(m, n, top, rng)
        t0 = time.time()
        best, ways, slots = count_by_pull(grid)
        elapsed = time.time() - t0
        cells = sum(1 for r in range(m) for c in range(n) if best[r][c] >= 0)
        digits = max(len(str(ways[r][c])) for r in range(m) for c in range(n))
        print(f"  {m}x{n}  {top:9d}  {cells:5d}  {slots:6d}  {slots / cells:5.2f}"
              f"  {elapsed:6.2f}s  {digits:26d}")

    print(f"\nall assertions held, {time.time() - started:.1f}s")
