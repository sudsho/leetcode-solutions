import itertools
import random
import time
from collections import deque
from typing import List

MOVES = ((1, 0), (-1, 0), (0, 1), (0, -1))


def parse(grid):
    """Start cell, a bit per litter cell, and the full mask."""
    start = None
    bits = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "L":
                bits[(r, c)] = 1 << len(bits)
    return start, bits, (1 << len(bits)) - 1


def search(grid, energy, mark=None, record=None):
    """BFS by moves on (cell, mask, energy), with three coarser marks.

    mark=None settles every (cell, mask, energy) once, the real search.
    mark="best" is the dominance mark, the standard solution: one entry per
    (cell, mask) holding the most energy seen there, reopened when a later
    arrival brings more. mark="first" is 1263's one mark per box cell: the
    first arrival at a (cell, mask) claims it and every later arrival, more
    energy or not, is refused. mark="cell" claims the cell alone and ignores
    the mask, the coarsest mark there is.

    record, if given, is a dict for the "first" run: it gets each refusal as
    (refused state, its move count in this run, the claimer's move count).
    """
    start, bits, full = parse(grid)
    if full == 0:
        return 0
    rows, cols = len(grid), len(grid[0])
    s = (start[0], start[1], 0, energy)
    seen = {s}
    best = {}
    claimed = {}
    q = deque([(s, 0)])
    while q:
        (r, c, mask, e), d = q.popleft()
        key = (r, c, mask) if mark != "cell" else (r, c)
        if mark in ("first", "cell"):
            if key in claimed:
                if record is not None:
                    record.setdefault("refused", []).append(((r, c, mask, e), d, claimed[key]))
                continue
            claimed[key] = d
        if e == 0:
            continue
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "X":
                continue
            nmask = mask | bits.get((nr, nc), 0)
            ne = energy if grid[nr][nc] == "R" else e - 1
            if nmask == full:
                return d + 1
            ns = (nr, nc, nmask, ne)
            if mark == "best":
                if best.get((nr, nc, nmask), -1) >= ne:
                    continue
                best[(nr, nc, nmask)] = ne
            elif ns in seen:
                continue
            seen.add(ns)
            q.append((ns, d + 1))
    return -1


def distances(grid, energy):
    """Every (cell, mask, energy) state's true move count, from the real search run to the end."""
    start, bits, full = parse(grid)
    rows, cols = len(grid), len(grid[0])
    s = (start[0], start[1], 0, energy)
    dist = {s: 0}
    q = deque([s])
    while q:
        r, c, mask, e = st = q.popleft()
        if e == 0 or mask == full:
            continue
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "X":
                continue
            ns = (nr, nc, mask | bits.get((nr, nc), 0), energy if grid[nr][nc] == "R" else e - 1)
            if ns not in dist:
                dist[ns] = dist[st] + 1
                q.append(ns)
    return dist


def real_tie(dist):
    """Whether some (cell, mask) is first reached at one move count by two different energies."""
    first = {}
    for (r, c, mask, e), d in dist.items():
        key = (r, c, mask)
        if key not in first or d < first[key][0]:
            first[key] = (d, {e})
        elif d == first[key][0]:
            first[key][1].add(e)
    return any(len(es) > 1 for _, es in first.values())


class Solution:
    def minMoves(self, classroom: List[str], energy: int) -> int:
        return search(classroom, energy, mark="best")


def all_boards(rows, cols, max_litter=3):
    """Every board with S in the corner and the other cells from . X L R, at most max_litter L."""
    n = rows * cols - 1
    for cells in itertools.product(".XLR", repeat=n):
        if cells.count("L") > max_litter:
            continue
        flat = ("S",) + cells
        yield ["".join(flat[r * cols:(r + 1) * cols]) for r in range(rows)]


def random_board(rng, rows, cols, litter, walls=0.2, resets=0.1):
    cells = []
    for _ in range(rows * cols - 1):
        u = rng.random()
        cells.append("X" if u < walls else "R" if u < walls + resets else ".")
    for i in rng.sample(range(len(cells)), litter):
        cells[i] = "L"
    flat = ["S"] + cells
    return ["".join(flat[r * cols:(r + 1) * cols]) for r in range(rows)]


def study(boards, energies, label):
    """One mark against the real search on every board at every energy, failures split by the tie."""
    sol = Solution()
    for energy in energies:
        n = solvable = best_off = multi = multi_cell = 0
        fail = {"first": 0, "cell": 0}
        minus = long = tie_real = tie_own = neither = refused = drift = 0
        witness = None
        for grid in boards:
            n += 1
            want = search(grid, energy)
            best_off += sol.minMoves(grid, energy) != want
            if want < 0:
                continue
            solvable += 1
            litter = sum(row.count("L") for row in grid) >= 2
            multi += litter
            rec = {}
            got = search(grid, energy, mark="first", record=rec)
            dist = None
            for st, d, _ in rec.get("refused", []):
                refused += 1
                if dist is None:
                    dist = distances(grid, energy)
                drift += d > dist[st]
            if got != want:
                fail["first"] += 1
                minus += got < 0
                long += got > want
                own = any(d == dc for _, d, dc in rec["refused"])
                real = real_tie(dist)
                tie_real += real
                tie_own += own and not real
                neither += not own and not real
                if witness is None:
                    witness = (grid, want, got)
            cell_wrong = search(grid, energy, mark="cell") != want
            fail["cell"] += cell_wrong
            multi_cell += cell_wrong and litter
        print(f"  {label} energy {energy}: {n} boards, {solvable} solvable, solution off {best_off}, "
              f"one mark per (cell, mask) wrong {fail['first']} ({minus} say -1, {long} too long; "
              f"real tie {tie_real}, own tie only {tie_own}, neither {neither}), "
              f"one mark per cell wrong {fail['cell']} ({multi_cell} of the {multi} with 2+ litter), "
              f"refusals {refused} of which drifted {drift}")
        if witness is not None:
            g, want, got = witness
            print(f"    witness {g}: answer {want}, one mark {got}")


if __name__ == "__main__":
    t0 = time.time()
    s = Solution()
    print("examples", s.minMoves(["S.", "XL"], 2), s.minMoves(["LS", "RL"], 4),
          s.minMoves(["L.S", "RXL"], 3), "want 2 3 -1")

    print("\nexhaustive, S in the corner, at most 3 litter")
    for rows, cols in ((2, 3), (2, 4), (3, 3)):
        boards = list(all_boards(rows, cols))
        study(boards, (2, 3, 4, 6, 20), f"{rows} x {cols}")

    print("\nrandom, 2000 boards at each size, 3 litter, a fifth walls, a tenth resets")
    rng = random.Random(3568)
    for rows, cols in ((4, 4), (5, 5), (6, 6)):
        boards = [random_board(rng, rows, cols, 3) for _ in range(2000)]
        study(boards, (4, 8, 16), f"{rows} x {cols}")

    print("\ntime at the statement's size, 20 x 20, 10 litter, 5 boards")
    boards = [random_board(rng, 20, 20, 10, walls=0.15, resets=0.05) for _ in range(5)]
    for name, fn in (("dominance mark", lambda g: s.minMoves(g, 50)), ("full state", lambda g: search(g, 50))):
        tt = time.perf_counter()
        for g in boards:
            fn(g)
        print(f"  {name:15s} {1000 * (time.perf_counter() - tt) / len(boards):.0f} ms")

    print(f"\n{time.time() - t0:.0f} s")
