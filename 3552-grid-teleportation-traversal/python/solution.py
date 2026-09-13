import heapq
from collections import deque
from typing import Dict, List, Tuple

Cell = Tuple[int, int]
INF = float("inf")


def buckets_of(matrix: List[str]) -> Dict[str, List[Cell]]:
    buckets: Dict[str, List[Cell]] = {}
    for r, row in enumerate(matrix):
        for c, ch in enumerate(row):
            if ch.isalpha():
                buckets.setdefault(ch, []).append((r, c))
    return buckets


def moves_from(matrix: List[str], r: int, c: int):
    m, n = len(matrix), len(matrix[0])
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < m and 0 <= cc < n and matrix[rr][cc] != "#":
            yield rr, cc


def oracle(matrix: List[str]):
    """Per-cell minimum moves and shortest-journey counts, with the rule in the state.

    A state is `(cell, letters used)`, so "each letter at most once" is enforced
    by the graph rather than by any line that could be deleted. A teleport sets a
    bit, which makes the zero-cost edges acyclic inside a level, and the counts
    are pushed over tight edges in `(dist, letters used)` order after the
    distances are finished, so no visiting order leaks into them. Returns
    `(best, count, walked)`, `walked` being the journeys whose last action is a
    move.
    """
    m, n = len(matrix), len(matrix[0])
    buckets = buckets_of(matrix)
    bit = {ch: 1 << k for k, ch in enumerate(sorted(buckets))}

    def successors(state):
        (r, c), used = state
        ch = matrix[r][c]
        if ch in bit and not used & bit[ch]:
            for cell in buckets[ch]:
                if cell != (r, c):
                    yield 0, (cell, used | bit[ch])
        for cell in moves_from(matrix, r, c):
            yield 1, (cell, used)

    start = ((0, 0), 0)
    dist = {start: 0}
    heap = [(0, 0, start)]
    while heap:
        d, _, state = heapq.heappop(heap)
        if d > dist[state]:
            continue
        for w, nxt in successors(state):
            if d + w < dist.get(nxt, INF):
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, bin(nxt[1]).count("1"), nxt))

    ways = {state: 0 for state in dist}
    by_move = {state: 0 for state in dist}
    ways[start] = 1
    by_move[start] = 1
    for state in sorted(dist, key=lambda s: (dist[s], bin(s[1]).count("1"))):
        for w, nxt in successors(state):
            if dist[nxt] == dist[state] + w:
                ways[nxt] += ways[state]
                if w == 1:
                    by_move[nxt] += ways[state]

    best = [[INF] * n for _ in range(m)]
    count = [[0] * n for _ in range(m)]
    walked = [[0] * n for _ in range(m)]
    for ((r, c), _), d in dist.items():
        best[r][c] = min(best[r][c], d)
    for ((r, c), used), d in dist.items():
        if d == best[r][c]:
            count[r][c] += ways[((r, c), used)]
            walked[r][c] += by_move[((r, c), used)]
    return best, count, walked


def min_moves(matrix: List[str], clear: bool = True) -> Tuple[int, int]:
    """The 0-1 bfs, instrumented, with the bucket clear switchable.

    Returns `(answer, scanned)`, where `scanned` counts bucket members looked at.
    With `clear=False` a letter can be used any number of times, so deleting the
    line is also deleting the rule from the statement.
    """
    m, n = len(matrix), len(matrix[0])
    buckets = buckets_of(matrix)
    dist = [[INF] * n for _ in range(m)]
    dist[0][0] = 0
    queue = deque([(0, 0, 0)])
    scanned = 0
    while queue:
        d, r, c = queue.popleft()
        if d > dist[r][c]:
            continue
        ch = matrix[r][c]
        if ch in buckets:
            for rr, cc in buckets[ch]:
                scanned += 1
                if d < dist[rr][cc]:
                    dist[rr][cc] = d
                    queue.appendleft((d, rr, cc))
            if clear:
                del buckets[ch]
        for rr, cc in moves_from(matrix, r, c):
            if d + 1 < dist[rr][cc]:
                dist[rr][cc] = d + 1
                queue.append((d + 1, rr, cc))
    answer = dist[m - 1][n - 1]
    return (-1 if answer == INF else int(answer)), scanned


def count_moves(matrix: List[str], clear: bool, read: str):
    """The same bfs counting shortest journeys, two switches.

    `clear` is the line. `read` is what a portal pop hands the other members:
    `"copy"` is the counting program everyone writes first - the pop's own count,
    set on first reach and `+=` on a tie, exactly 1871's and 1345's `elif`.
    `"walk_sum"` sums the walking arrivals over every member already at this
    level and overwrites each member's teleport count with that sum minus its own.

    Counts are split into `walk` (last action a move) and `tele` (last action a
    teleport), because a teleport may only follow a move - the next teleport out
    of a portal would reuse its letter. Returns `(dist, walk, tele, scanned)`.
    """
    m, n = len(matrix), len(matrix[0])
    buckets = buckets_of(matrix)
    dist = [[INF] * n for _ in range(m)]
    walk = [[0] * n for _ in range(m)]
    tele = [[0] * n for _ in range(m)]
    dist[0][0] = 0
    walk[0][0] = 1
    queue = deque([(0, 0, 0)])
    scanned = 0
    while queue:
        d, r, c = queue.popleft()
        if d > dist[r][c]:
            continue
        ch = matrix[r][c]
        if ch in buckets:
            members = buckets[ch]
            if read == "copy":
                total = walk[r][c] + tele[r][c]
                for rr, cc in members:
                    if (rr, cc) == (r, c):
                        continue
                    scanned += 1
                    if d < dist[rr][cc]:
                        dist[rr][cc] = d
                        walk[rr][cc] = 0
                        tele[rr][cc] = total
                        queue.appendleft((d, rr, cc))
                    elif d == dist[rr][cc]:
                        tele[rr][cc] += total
            else:
                arrived = 0
                for rr, cc in members:
                    scanned += 1
                    if dist[rr][cc] == d:
                        arrived += walk[rr][cc]
                for rr, cc in members:
                    scanned += 1
                    if d < dist[rr][cc]:
                        dist[rr][cc] = d
                        walk[rr][cc] = 0
                        tele[rr][cc] = arrived
                        queue.appendleft((d, rr, cc))
                    elif d == dist[rr][cc]:
                        tele[rr][cc] = arrived - walk[rr][cc]
            if clear:
                del buckets[ch]
        total = walk[r][c] + tele[r][c]
        for rr, cc in moves_from(matrix, r, c):
            if d + 1 < dist[rr][cc]:
                dist[rr][cc] = d + 1
                walk[rr][cc] = total
                tele[rr][cc] = 0
                queue.append((d + 1, rr, cc))
            elif d + 1 == dist[rr][cc]:
                walk[rr][cc] += total
    return dist, walk, tele, scanned


def count_min_jumps_1345_by_levels(arr: List[int], subtract: bool = True):
    """1345's shortest-sequence count keeping the clear, level by level.

    A bucket's members all sit within one level of its lowest member - every one
    of them is a single jump from it. So when the first member shows up in a
    frontier, everything that bucket will ever contribute is the frontier's
    members' summed ways, handed to the members one level down. One pass per
    bucket. A member adjacent to a frontier member of its own bucket is reached
    by both edges but the pair is one index sequence, so that member's own
    neighbours are taken back out of the sum. Returns `(ways, scanned, dist)`.
    """
    n = len(arr)
    by_value: Dict[int, List[int]] = {}
    for i, value in enumerate(arr):
        by_value.setdefault(value, []).append(i)
    dist = [-1] * n
    ways = [0] * n
    dist[0] = 0
    ways[0] = 1
    frontier = [0]
    level = 0
    scanned = 0
    while frontier:
        nxt: List[int] = []
        summed: Dict[int, int] = {}
        for i in frontier:
            if arr[i] in by_value:
                summed[arr[i]] = summed.get(arr[i], 0) + ways[i]
        for i in frontier:
            for j in (i - 1, i + 1):
                if 0 <= j < n:
                    scanned += 1
                    if dist[j] < 0:
                        dist[j] = level + 1
                        ways[j] = ways[i]
                        nxt.append(j)
                    elif dist[j] == level + 1:
                        ways[j] += ways[i]
        for value, total in summed.items():
            for j in by_value.pop(value):
                scanned += 1
                if dist[j] >= 0 and dist[j] <= level:
                    continue
                share = total - subtract * sum(
                    ways[k] for k in (j - 1, j + 1)
                    if 0 <= k < n and arr[k] == value and dist[k] == level
                )
                if dist[j] < 0:
                    dist[j] = level + 1
                    ways[j] = share
                    nxt.append(j)
                else:
                    ways[j] += share
        frontier = nxt
        level += 1
    return ways[n - 1], scanned, dist


class Solution:
    def minMoves(self, matrix: List[str]) -> int:
        """Minimum moves from the top-left to the bottom-right, where standing on
        a portal whose letter is unused lets you teleport free to any other cell
        with that letter, each letter at most once.

        Taken for the 12th's open item. 1871 kept its skip under counting because
        distance there is monotone in the index, and 1345 has no such order, so
        its replacement was still unwritten. This is 1345's bucket clear with one
        change, that a teleport costs nothing, so a letter's portals land on one
        level instead of two. The statement also writes the clear down as a rule,
        and for the minimum the rule is a line the proof never needs: a shortest
        route never teleports on one letter twice with a move in between, because
        the second teleport could have been taken from the first portal. Without
        it the answer is unchanged on every grid over `.#AB` up to 3x3, and the
        bucket scan is `N^2` against `N` on an all-portal grid. Counting, and
        1345's replacement, are run in `__main__`.
        """
        n = len(matrix[0])
        m = len(matrix)
        buckets = buckets_of(matrix)
        dist = [[INF] * n for _ in range(m)]
        dist[0][0] = 0
        queue = deque([(0, 0, 0)])
        while queue:
            d, r, c = queue.popleft()
            if d > dist[r][c]:
                continue
            if (r, c) == (m - 1, n - 1):
                return d
            ch = matrix[r][c]
            # popping the bucket is the at-most-once rule. deleting it leaves
            # every answer alone and makes the scan quadratic in the class size.
            if ch in buckets:
                for rr, cc in buckets.pop(ch):
                    if d < dist[rr][cc]:
                        dist[rr][cc] = d
                        queue.appendleft((d, rr, cc))
            for rr, cc in moves_from(matrix, r, c):
                if d + 1 < dist[rr][cc]:
                    dist[rr][cc] = d + 1
                    queue.append((d + 1, rr, cc))
        return -1


if __name__ == "__main__":
    import importlib.util
    import itertools
    import os
    import random
    import time

    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "jump_game_vii", os.path.join(here, "..", "..", "1871-jump-game-vii", "python", "solution.py"))
    jump_game_vii = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(jump_game_vii)
    oracle_1345 = jump_game_vii.oracle_1345

    def has_tie(grid, best, walked):
        """Two or more members of one letter walked into at that letter's level."""
        return any(
            sum(best[r][c] < INF and walked[r][c] > 0 for r, c in members) > 1
            for members in buckets_of(grid).values()
        )

    started = time.time()
    solution = Solution()

    print("answers")
    for grid, expected in (
        (["A..", ".A.", "..."], 2),
        ([".#...", ".#.#.", ".#.#.", "...#."], 13),
        (["."], 0),
        ([".#", "#."], -1),
        (["A#", "#A"], 0),
    ):
        got = solution.minMoves(grid)
        assert got == expected, (grid, got)
        print(f"  {grid!s:40s} {got}")

    print("\nexhaustively, every grid over '.#AB' with a free start")
    for m, n in ((2, 3), (2, 4), (3, 3)):
        stats = dict(grids=0, reachable=0, shortened=0, tied=0, keep_copy=0, drop_copy_over=0,
                     drop_copy_under=0, keep_sum=0, drop_sum=0, letters=0)
        for cells in itertools.product(".#AB", repeat=m * n - 1):
            for first in ".AB":
                flat = first + "".join(cells)
                grid = [flat[k * n:(k + 1) * n] for k in range(m)]
                best, count, walked = oracle(grid)
                truth = best[m - 1][n - 1]
                truth = -1 if truth == INF else truth
                kept, _ = min_moves(grid, clear=True)
                dropped, _ = min_moves(grid, clear=False)
                assert kept == dropped == truth, (grid, kept, dropped, truth)
                assert solution.minMoves(grid) == truth
                stats["grids"] += 1
                if truth < 0:
                    continue
                stats["reachable"] += 1
                plain, _ = min_moves([row.replace("A", ".").replace("B", ".") for row in grid])
                stats["shortened"] += plain != truth
                for members in buckets_of(grid).values():
                    reached = [(r, c) for r, c in members if best[r][c] < INF]
                    if len(reached) > 1:
                        # one level per letter, and one count per letter.
                        assert len({best[r][c] for r, c in reached}) == 1, grid
                        assert len({count[r][c] for r, c in reached}) == 1, grid
                        stats["letters"] += 1
                tied = has_tie(grid, best, walked)
                stats["tied"] += tied
                target = count[m - 1][n - 1]

                _, walk, tele, _ = count_moves(grid, True, "copy")
                got = walk[m - 1][n - 1] + tele[m - 1][n - 1]
                assert got <= target, grid
                stats["keep_copy"] += got != target
                if not tied:
                    assert all(walk[r][c] + tele[r][c] == count[r][c]
                               for r in range(m) for c in range(n) if best[r][c] < INF), grid

                _, walk, tele, _ = count_moves(grid, False, "copy")
                got = walk[m - 1][n - 1] + tele[m - 1][n - 1]
                stats["drop_copy_over"] += got > target
                stats["drop_copy_under"] += got < target

                for key, clear in (("keep_sum", True), ("drop_sum", False)):
                    _, walk, tele, _ = count_moves(grid, clear, "walk_sum")
                    for r in range(m):
                        for c in range(n):
                            if best[r][c] < INF:
                                assert walk[r][c] == walked[r][c], (grid, key, r, c)
                                assert walk[r][c] + tele[r][c] == count[r][c], (grid, key, r, c)
        print(f"  {m}x{n}  {stats}")

    print("\nscans on an all-portal grid, N cells")
    for side in (3, 10, 30, 60):
        grid = ["A" * side] * side
        _, kept = min_moves(grid, clear=True)
        _, dropped = min_moves(grid, clear=False)
        total = side * side
        assert kept == total and dropped == total * total
        print(f"  N={total:5d}  clear={kept:6d}  no clear={dropped:8d}  N^2={total * total:8d}")

    random.seed(13)
    print("\nrandom 6x6 grids, 20% walls")
    for letters, portal_rate in ((1, 0.2), (2, 0.2), (3, 0.3), (6, 0.5), (26, 0.5)):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:letters]
        reachable = shortened = tied = keep_wrong = keep_wrong_shortened = drop_wrong = 0
        for _ in range(400):
            rows = []
            for r in range(6):
                row = ""
                for c in range(6):
                    x = random.random()
                    if (r, c) != (0, 0) and x < 0.2:
                        row += "#"
                    elif x < 0.2 + portal_rate * 0.8:
                        row += random.choice(alphabet)
                    else:
                        row += "."
                rows.append(row)
            best, count, walked = oracle(rows)
            if best[5][5] == INF:
                continue
            reachable += 1
            plain, _ = min_moves(["".join("." if ch.isalpha() else ch for ch in row) for row in rows])
            teleports = plain != best[5][5]
            shortened += teleports
            tie = has_tie(rows, best, walked)
            tied += tie
            _, walk, tele, _ = count_moves(rows, True, "copy")
            wrong = walk[5][5] + tele[5][5] != count[5][5]
            assert tie or not wrong, rows
            keep_wrong += wrong
            keep_wrong_shortened += wrong and teleports
            _, walk, tele, _ = count_moves(rows, False, "copy")
            drop_wrong += walk[5][5] + tele[5][5] != count[5][5]
            for clear in (True, False):
                _, walk, tele, _ = count_moves(rows, clear, "walk_sum")
                assert walk[5][5] + tele[5][5] == count[5][5], rows
        print(f"  letters={letters:2d} portals={portal_rate:.1f}  reachable {reachable:3d}/400"
              f"  teleport shortens {shortened:3d}  tie {tied:3d}  keep+copy wrong {keep_wrong:3d}"
              f" ({keep_wrong_shortened:3d} shortened)  drop+copy wrong {drop_wrong:3d}")

    print("\nno clear / clear on random 60x60 grids, 10% walls, 50% portals")
    for letters in (26, 8, 3, 1):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:letters]
        ratios = []
        for _ in range(5):
            rows = [
                "".join(
                    "#" if (r, c) != (0, 0) and random.random() < 0.1
                    else (random.choice(alphabet) if random.random() < 0.5 else ".")
                    for c in range(60)
                )
                for r in range(60)
            ]
            a, kept = min_moves(rows, clear=True)
            b, dropped = min_moves(rows, clear=False)
            assert a == b
            ratios.append(dropped / max(kept, 1))
        print(f"  letters={letters:2d}  ratio={sum(ratios) / len(ratios):8.2f}x")

    print("\n1345, counting with the clear kept, one pass per bucket")
    for alphabet, length in ((2, 10), (3, 7)):
        total = unsubtracted_wrong = 0
        for values in itertools.product(range(alphabet), repeat=length):
            values = list(values)
            truth = oracle_1345(values)
            got, _, dist = count_min_jumps_1345_by_levels(values)
            assert got == truth, values
            for value in set(values):
                levels = [dist[i] for i in range(length) if values[i] == value]
                assert max(levels) - min(levels) <= 1, values
            unsubtracted_wrong += count_min_jumps_1345_by_levels(values, subtract=False)[0] != truth
            total += 1
        print(f"  |values|={alphabet} length={length}  {total} arrays, wrong 0, every bucket within"
              f" one level   without the neighbour correction wrong {unsubtracted_wrong}")
    for distinct in (60, 20, 8, 3, 1):
        worst = 0.0
        unsubtracted_wrong = 0
        for _ in range(300):
            values = [random.randrange(distinct) for _ in range(60)]
            truth = oracle_1345(values)
            got, scanned, _ = count_min_jumps_1345_by_levels(values)
            assert got == truth, values
            unsubtracted_wrong += count_min_jumps_1345_by_levels(values, subtract=False)[0] != truth
            worst = max(worst, scanned / len(values))
        print(f"  |distinct values|={distinct:3d}  300 random arrays of 60, wrong 0,"
              f"  worst scanned/n {worst:.2f}   without the correction wrong {unsubtracted_wrong}")
    print(f"\n{time.time() - started:.0f}s")
