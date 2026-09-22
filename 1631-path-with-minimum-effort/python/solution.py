import heapq
import itertools
import random
import time
from collections import deque
from typing import List, Tuple

Grid = List[List[int]]
MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def neighbours(rows: int, cols: int, r: int, c: int):
    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def dijkstra(heights: Grid, relation: str = "max", on_push: bool = False) -> int:
    """Least effort from the top-left to the bottom-right, settling the smallest first.

    `relation` is "max" for the problem (the effort of a route is its largest
    step) or "sum" for total climb, which is 1514's argument back on a sum.
    Both are non-improving: `max(e, w) >= e` and `e + w >= e` for `w >= 0`.
    The difference is that the max often leaves the value exactly where it
    was, so a lot of the relaxations write the popped value straight through.

    `on_push` returns the first time the target is written instead of when it
    pops, which is the early exit that is wrong for a sum and is the question
    for a max.
    """
    rows, cols = len(heights), len(heights[0])
    target = (rows - 1, cols - 1)
    best = {(0, 0): 0}
    done = set()
    heap = [(0, 0, 0)]
    while heap:
        e, r, c = heapq.heappop(heap)
        if (r, c) in done:
            continue
        if (r, c) == target:
            return e
        done.add((r, c))
        for nr, nc in neighbours(rows, cols, r, c):
            w = abs(heights[nr][nc] - heights[r][c])
            nxt = max(e, w) if relation == "max" else e + w
            if nxt < best.get((nr, nc), float("inf")):
                best[(nr, nc)] = nxt
                if on_push and (nr, nc) == target:
                    return nxt
                heapq.heappush(heap, (nxt, nr, nc))
    return best.get(target, 0)


def union_find(heights: Grid) -> int:
    """Kruskal until the corners join. The last edge added is the answer.

    A minimax route between two nodes can always be taken inside a minimum
    spanning tree, so sorting the edges and joining until the corners are in
    one set gives the bottleneck with no heap and no settle at all.
    """
    rows, cols = len(heights), len(heights[0])
    if rows * cols == 1:
        return 0
    parent = list(range(rows * cols))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = []
    for r in range(rows):
        for c in range(cols):
            if r + 1 < rows:
                edges.append((abs(heights[r + 1][c] - heights[r][c]), r * cols + c, (r + 1) * cols + c))
            if c + 1 < cols:
                edges.append((abs(heights[r][c + 1] - heights[r][c]), r * cols + c, r * cols + c + 1))
    edges.sort()
    for w, a, b in edges:
        parent[find(a)] = find(b)
        if find(0) == find(rows * cols - 1):
            return w
    raise AssertionError("a grid is connected")


def binary_search(heights: Grid) -> int:
    """Smallest limit at which a BFS over steps <= limit reaches the corner."""
    rows, cols = len(heights), len(heights[0])

    def reaches(limit: int) -> bool:
        seen = {(0, 0)}
        queue = deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            if (r, c) == (rows - 1, cols - 1):
                return True
            for nr, nc in neighbours(rows, cols, r, c):
                if (nr, nc) not in seen and abs(heights[nr][nc] - heights[r][c]) <= limit:
                    seen.add((nr, nc))
                    queue.append((nr, nc))
        return False

    lo, hi = 0, max(map(max, heights)) - min(map(min, heights))
    while lo < hi:
        mid = (lo + hi) // 2
        if reaches(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def right_down(heights: Grid) -> int:
    """The DP that only moves right and down. It searches a subset of the routes, so it can only be too big."""
    rows, cols = len(heights), len(heights[0])
    inf = float("inf")
    dp = [[inf] * cols for _ in range(rows)]
    dp[0][0] = 0
    for r in range(rows):
        for c in range(cols):
            if r:
                dp[r][c] = min(dp[r][c], max(dp[r - 1][c], abs(heights[r][c] - heights[r - 1][c])))
            if c:
                dp[r][c] = min(dp[r][c], max(dp[r][c - 1], abs(heights[r][c] - heights[r][c - 1])))
    return dp[-1][-1]


def oracle(heights: Grid) -> Tuple[int, int, int]:
    """Every simple route between the corners: (best max, best sum, routes attaining the best max).

    No heap and no settle. Both relations are non-decreasing along a route, so
    a repeated cell never helps either, and the simple routes hold the answers.
    """
    rows, cols = len(heights), len(heights[0])
    target = (rows - 1, cols - 1)
    best_max = best_sum = float("inf")
    attaining = 0
    stack = [((0, 0), 0, 0, 1)]
    while stack:
        (r, c), m, s, seen = stack.pop()
        if (r, c) == target:
            if m < best_max:
                best_max, attaining = m, 0
            attaining += m == best_max
            best_sum = min(best_sum, s)
            continue
        for nr, nc in neighbours(rows, cols, r, c):
            bit = 1 << (nr * cols + nc)
            if not seen & bit:
                w = abs(heights[nr][nc] - heights[r][c])
                stack.append(((nr, nc), max(m, w), s + w, seen | bit))
    return best_max, best_sum, attaining


class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        """Dijkstra on the largest step. The two alternatives and the early exit are in `__main__`."""
        return dijkstra(heights)


def grids(rows: int, cols: int, values: Tuple[int, ...]):
    for cells in itertools.product(values, repeat=rows * cols):
        yield [list(cells[r * cols:(r + 1) * cols]) for r in range(rows)]


if __name__ == "__main__":
    rng = random.Random(1631)
    started = time.time()

    print("== exhaustive, against every simple route ==")
    print("  shape  values     grids   tied   dijkstra  union-find  bisect   right/down wrong (too big)"
          "   on-push wrong: max   sum")
    for (rows, cols), values in (((2, 2), (0, 1, 2, 3)), ((2, 3), (0, 1, 2)), ((3, 3), (0, 1, 2)),
                                 ((2, 5), (0, 1, 2)), ((3, 4), (0, 1))):
        total = tied = 0
        wrong = [0, 0, 0]
        rd_wrong = rd_big = push_max = push_sum = 0
        for g in grids(rows, cols, values):
            total += 1
            truth, truth_sum, attaining = oracle(g)
            tied += attaining > 1
            for k, f in enumerate((dijkstra, union_find, binary_search)):
                wrong[k] += f(g) != truth
            assert dijkstra(g, "sum") == truth_sum
            rd = right_down(g)
            rd_wrong += rd != truth
            rd_big += rd > truth
            push_max += dijkstra(g, "max", on_push=True) != truth
            push_sum += dijkstra(g, "sum", on_push=True) != truth_sum
        print(f"  {rows}x{cols}    {str(values):10s} {total:6d} {tied:6d}   {wrong[0]:6d}   {wrong[1]:8d}  {wrong[2]:6d}"
              f"   {rd_wrong:6d} ({rd_big})              {push_max:6d} {push_sum:6d}")

    print("\n== random grids, the three methods against each other ==")
    for size, top, count in ((10, 10, 2000), (30, 1000, 300), (100, 10 ** 6, 20)):
        disagree = rd_wrong = 0
        for _ in range(count):
            g = [[rng.randint(1, top) for _ in range(size)] for _ in range(size)]
            a = dijkstra(g)
            disagree += not (a == union_find(g) == binary_search(g))
            rd_wrong += right_down(g) != a
        print(f"  {size}x{size} heights 1..{top}  grids {count}   methods disagree {disagree}"
              f"   right/down wrong {rd_wrong}")

    print("\n== the statement's size, timed ==")
    s = Solution()
    for label, g in (("random 1..1e6", [[rng.randint(1, 10 ** 6) for _ in range(100)] for _ in range(100)]),
                     ("all equal", [[7] * 100 for _ in range(100)]),
                     # walls on odd rows with one gap at alternating ends, 99 rows so the corner is not
                     # in a wall: the only flat route is about 5000 cells long.
                     ("snake", [[10 ** 6 if (r % 4 == 1 and c < 99) or (r % 4 == 3 and c > 0) else 0
                                 for c in range(100)] for r in range(99)])):
        for name, f in (("dijkstra", s.minimumEffortPath), ("union-find", union_find), ("bisect", binary_search)):
            t0 = time.time()
            ans = f(g)
            print(f"  {label:14s} {name:10s} answer {ans:7d}   {time.time() - t0:.3f}s")

    print(f"\n{time.time() - started:.0f}s")
