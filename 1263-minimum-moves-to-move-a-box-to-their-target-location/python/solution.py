import itertools
import random
import time
from collections import deque
from typing import List

# up, right, down, left. A push in direction d needs the player on the cell behind the box, opposite d.
DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))


class Board:
    """The grid as cell indices, with nbr[d][i] the cell one step from i in direction d, or -1 for a wall or the edge."""

    def __init__(self, grid):
        self.rows, self.cols = len(grid), len(grid[0])
        cells = self.rows * self.cols
        self.free = [grid[i // self.cols][i % self.cols] != "#" for i in range(cells)]
        for i in range(cells):
            ch = grid[i // self.cols][i % self.cols]
            if ch == "S":
                self.player = i
            elif ch == "B":
                self.box = i
            elif ch == "T":
                self.target = i
        self.nbr = [[-1] * cells for _ in DIRS]
        for i in range(cells):
            r, c = divmod(i, self.cols)
            for d, (dr, dc) in enumerate(DIRS):
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols and self.free[rr * self.cols + cc]:
                    self.nbr[d][i] = rr * self.cols + cc
        self._labels = {}

    def reach(self, start, box):
        """Cells the player can walk to from start with the box standing on box, as a set."""
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for d in range(4):
                w = self.nbr[d][u]
                if w >= 0 and w != box and w not in seen:
                    seen.add(w)
                    stack.append(w)
        return seen

    def labels(self, box):
        """Component label of every free cell with the box on box, the smallest index in its component. Cached per box cell."""
        lab = self._labels.get(box)
        if lab is None:
            lab = [-1] * len(self.free)
            for i in range(len(self.free)):
                if self.free[i] and i != box and lab[i] < 0:
                    for j in self.reach(i, box):
                        lab[j] = i
            self._labels[box] = lab
        return lab


def by_side(grid, counter=None, order=(0, 1, 2, 3)):
    """BFS on (box, player), one mark per pair, a flood fill at every pop. The textbook search.

    After the first push the player always stands where the box was, so the
    pair is (box, side) and there are at most four marks per box cell.
    """
    g = Board(grid)
    if g.box == g.target:
        return 0
    seen = {(g.box, g.player)}
    queue = deque([(g.box, g.player, 0)])
    while queue:
        b, p, k = queue.popleft()
        if counter is not None:
            counter[0] += 1
        region = g.reach(p, b)
        for d in order:
            ahead, behind = g.nbr[d][b], g.nbr[(d + 2) % 4][b]
            if ahead >= 0 and behind in region and (ahead, b) not in seen:
                if ahead == g.target:
                    return k + 1
                seen.add((ahead, b))
                queue.append((ahead, b, k + 1))
    return -1


def by_component(grid, counter=None, order=(0, 1, 2, 3)):
    """BFS on (box, component the player is in), one mark per component.

    Two player cells in the same component, with the box where it is, can walk
    to each other for free, so each stands in for the other completely. The
    second coordinate is neither ordered nor unordered here, it is a quotient,
    and the bar is one mark per class. The labels are computed once per box
    cell and a push is a table lookup.
    """
    g = Board(grid)
    if g.box == g.target:
        return 0
    start = (g.box, g.labels(g.box)[g.player])
    seen = {start}
    queue = deque([(start[0], start[1], 0)])
    while queue:
        b, comp, k = queue.popleft()
        if counter is not None:
            counter[0] += 1
        lab = g.labels(b)
        for d in order:
            ahead, behind = g.nbr[d][b], g.nbr[(d + 2) % 4][b]
            if ahead >= 0 and behind >= 0 and lab[behind] == comp:
                if ahead == g.target:
                    return k + 1
                key = (ahead, g.labels(ahead)[b])
                if key not in seen:
                    seen.add(key)
                    queue.append((ahead, key[1], k + 1))
    return -1


def by_cell(grid, counter=None):
    """0-1 BFS on (box, player cell): a step costs 0, a push costs 1. No flood fill and no labels, and every cell a state."""
    g = Board(grid)
    best = {(g.box, g.player): 0}
    queue = deque([(g.box, g.player, 0)])
    while queue:
        b, p, k = queue.popleft()
        if best[(b, p)] < k:
            continue
        if counter is not None:
            counter[0] += 1
        if b == g.target:
            return k
        for d in range(4):
            w = g.nbr[d][p]
            if w < 0:
                continue
            if w != b:
                if best.get((b, w), k + 1) > k:
                    best[(b, w)] = k
                    queue.appendleft((b, w, k))
            else:
                ahead = g.nbr[d][b]
                if ahead >= 0 and best.get((ahead, b), k + 2) > k + 1:
                    best[(ahead, b)] = k + 1
                    queue.append((ahead, b, k + 1))
    return -1


def one_mark(grid, order=(0, 1, 2, 3)):
    """One mark per box cell, whichever side the player reached it from. Reads the player as if it did not matter."""
    g = Board(grid)
    if g.box == g.target:
        return 0
    seen = {g.box}
    queue = deque([(g.box, g.player, 0)])
    while queue:
        b, p, k = queue.popleft()
        region = g.reach(p, b)
        for d in order:
            ahead, behind = g.nbr[d][b], g.nbr[(d + 2) % 4][b]
            if ahead >= 0 and behind in region and ahead not in seen:
                if ahead == g.target:
                    return k + 1
                seen.add(ahead)
                queue.append((ahead, b, k + 1))
    return -1


def oracle(grid):
    """Every layer as the set of (box, player cell) after exactly k pushes, nothing marked across layers.

    Stops when a layer is empty or repeats an earlier one, since the next
    layer is a function of this one and a repeat means the target is never
    reached.
    """
    g = Board(grid)
    layer = frozenset((g.box, p) for p in g.reach(g.player, g.box))
    past = set()
    k = 0
    while layer and layer not in past:
        if any(b == g.target for b, _ in layer):
            return k
        past.add(layer)
        nxt = set()
        for b, p in layer:
            for d in range(4):
                if g.nbr[(d + 2) % 4][b] == p and g.nbr[d][b] >= 0:
                    nb = g.nbr[d][b]
                    nxt.update((nb, q) for q in g.reach(b, nb))
        layer = frozenset(nxt)
        k += 1
    return -1


class Solution:
    def minPushBox(self, grid: List[List[str]]) -> int:
        """BFS on (box, player component), labels cached per box cell. The rest is in `__main__`."""
        return by_component(grid)


def exhaustive(rows, cols):
    """Every wall set on rows x cols with S, B and T on three distinct free cells."""
    n = rows * cols
    for mask in range(1 << n):
        free = [i for i in range(n) if not mask >> i & 1]
        for s, b, t in itertools.permutations(free, 3):
            cells = ["#" if mask >> i & 1 else "." for i in range(n)]
            cells[s], cells[b], cells[t] = "S", "B", "T"
            yield [cells[r * cols:(r + 1) * cols] for r in range(rows)]


def random_instance(rng, rows, cols, wall):
    """Each cell a wall with probability wall, then S, B and T on three distinct free cells. Redrawn until three are free."""
    while True:
        cells = ["#" if rng.random() < wall else "." for _ in range(rows * cols)]
        free = [i for i, ch in enumerate(cells) if ch == "."]
        if len(free) >= 3:
            s, b, t = rng.sample(free, 3)
            cells[s], cells[b], cells[t] = "S", "B", "T"
            return [cells[r * cols:(r + 1) * cols] for r in range(rows)]


def symmetries(rows, cols):
    """The board's symmetries as permutations of DIRS: the four of a rectangle, eight when it is square."""
    rect = [lambda d: d, lambda d: (4 - d) % 4, lambda d: (2 - d) % 4, lambda d: (d + 2) % 4]
    if rows != cols:
        return rect
    return rect + [lambda d: (d + 1) % 4, lambda d: (d + 3) % 4, lambda d: (5 - d) % 4, lambda d: (3 - d) % 4]


EXAMPLES = [
    (["######", "#T####", "#..B.#", "#.##.#", "#...S#", "######"], 3),
    (["######", "#T####", "#..B.#", "####.#", "#...S#", "######"], -1),
    (["######", "#T..##", "#.#B.#", "#....#", "#...S#", "######"], 5),
]


if __name__ == "__main__":
    s = Solution()
    for rows, want in EXAMPLES:
        print(s.minPushBox([list(r) for r in rows]), "expect", want)

    t0 = time.time()
    print("\nexhaustive, against the layer oracle")
    for rows, cols in ((2, 4), (2, 5), (3, 3)):
        total = bad = wrong = 0
        smallest = None
        for grid in exhaustive(rows, cols):
            want = oracle(grid)
            total += 1
            got = (by_side(grid), by_component(grid), by_cell(grid))
            bad += any(x != want for x in got)
            if one_mark(grid) != want:
                wrong += 1
                walls = sum(ch == "#" for row in grid for ch in row)
                if smallest is None or walls > smallest[0]:
                    smallest = (walls, grid, want, one_mark(grid))
        print(f"  {rows}x{cols}: {total} instances, exact searches off on {bad}, "
              f"one mark wrong on {wrong} ({100 * wrong / total:.2f}%)")
        if smallest:
            print(f"    most walls among its failures: {smallest[0]}, "
                  f"{[''.join(r) for r in smallest[1]]} answer {smallest[2]} said {smallest[3]}")

    print("\none mark under all 24 push orders, grouped by symmetry orbit")
    for rows, cols in ((2, 5), (3, 3)):
        grids = list(exhaustive(rows, cols))
        truth = [oracle(gr) for gr in grids]
        orders = list(itertools.permutations(range(4)))
        wrong = {o: frozenset(i for i, gr in enumerate(grids) if one_mark(gr, o) != truth[i]) for o in orders}
        syms = symmetries(rows, cols)
        orbits = {}
        for o in orders:
            rep = min(tuple(f(d) for d in o) for f in syms)
            orbits.setdefault(rep, []).append(o)
        for rep, members in sorted(orbits.items()):
            counts = sorted({len(wrong[o]) for o in members})
            print(f"  {rows}x{cols} orbit of {rep}: {len(members)} orders, wrong counts {counts}")
        every = frozenset.intersection(*wrong.values())
        some = frozenset.union(*wrong.values())
        print(f"  {rows}x{cols}: wrong under every order {len(every)}, under some order {len(some)}")

    print("\nrandom, 4000 at each size and wall density, pops per instance")
    rng = random.Random(1263)
    for rows, cols in ((4, 4), (6, 6), (8, 8)):
        for wall in (0.0, 0.2, 0.35):
            n = 4000 if rows < 8 else 1500
            ps, pc, pb = [0], [0], [0]
            wrong = off = 0
            for _ in range(n):
                grid = random_instance(rng, rows, cols, wall)
                want = by_cell(grid, pb)
                off += by_side(grid, ps) != want or by_component(grid, pc) != want
                if rows == 4:
                    off += oracle(grid) != want
                wrong += one_mark(grid) != want
            print(f"  {rows}x{cols} walls {wall:.2f}: off {off}, one mark wrong {100 * wrong / n:5.2f}%, "
                  f"pops side {ps[0] / n:6.1f} component {pc[0] / n:6.1f} cell {pb[0] / n:7.1f}, "
                  f"component saves {100 * (1 - pc[0] / max(ps[0], 1)):4.1f}%")

    print("\ntime at 20x20, 200 instances at walls 0.2")
    grids = [random_instance(rng, 20, 20, 0.2) for _ in range(200)]
    for name, fn in (("side", by_side), ("component", by_component), ("cell", by_cell)):
        t = time.perf_counter()
        for gr in grids:
            fn(gr)
        print(f"  {name:9s} {1000 * (time.perf_counter() - t) / len(grids):.2f} ms")

    print(f"\n{time.time() - t0:.0f} s")
