import itertools
import random
import time
from collections import deque
from typing import List

MOVES = ((0, 1), (1, 0), (0, -1), (-1, 0))


def parse(grid):
    rows, cols = len(grid), len(grid[0])
    start, k = None, 0
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            if ch == "@":
                start = r * cols + c
            elif "a" <= ch <= "f":
                k += 1
    return rows, cols, start, k


def step(grid, rows, cols, cell, mask, moves=MOVES):
    """The states one move away from (cell, mask), as (cell, mask) pairs, in the order given."""
    r, c = divmod(cell, cols)
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue
        ch = grid[nr][nc]
        if ch == "#":
            continue
        if "A" <= ch <= "F" and not (mask >> (ord(ch) - 65)) & 1:
            continue
        nm = mask | (1 << (ord(ch) - 97)) if "a" <= ch <= "f" else mask
        yield nr * cols + nc, nm


def layered(grid, counter=None):
    """BFS on (cell, mask), each state visited once. The textbook search."""
    rows, cols, start, k = parse(grid)
    full = (1 << k) - 1
    if full == 0:
        return 0
    seen = [False] * (rows * cols << k)
    seen[start << k] = True
    queue = deque([(start, 0, 0)])
    while queue:
        cell, mask, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        for nc, nm in step(grid, rows, cols, cell, mask):
            if nm == full:
                return d + 1
            if not seen[nc << k | nm]:
                seen[nc << k | nm] = True
                queue.append((nc, nm, d + 1))
    return -1


def antichain_bar(grid, counter=None, widest=None):
    """2093's bar with a coordinate that is only partly ordered: a set of masks per cell, none a subset of another.

    A push at (cell, mask) is dropped when a superset of mask has already been
    queued at the cell, since that arrival is no later and can open every door
    this one can. A mask that survives evicts the subsets it dominates. Every
    move costs 1, so the queue is in cost order from the push and the bar goes
    on there, as in 1654.
    """
    rows, cols, start, k = parse(grid)
    full = (1 << k) - 1
    if full == 0:
        return 0
    front = [[] for _ in range(rows * cols)]
    front[start] = [0]
    queue = deque([(start, 0, 0)])
    while queue:
        cell, mask, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        for nc, nm in step(grid, rows, cols, cell, mask):
            if nm == full:
                return d + 1
            held = front[nc]
            if any(m & nm == nm for m in held):
                continue
            held[:] = [m for m in held if m & nm != m]
            held.append(nm)
            if widest is not None and len(held) > widest[0]:
                widest[0] = len(held)
            queue.append((nc, nm, d + 1))
    return -1


def count_bar(grid, moves=MOVES):
    """One number per cell, the most keys any queued arrival held. Flattens the partial order and is wrong."""
    rows, cols, start, k = parse(grid)
    full = (1 << k) - 1
    if full == 0:
        return 0
    best = [-1] * (rows * cols)
    best[start] = 0
    queue = deque([(start, 0, 0)])
    while queue:
        cell, mask, d = queue.popleft()
        for nc, nm in step(grid, rows, cols, cell, mask, moves):
            if nm == full:
                return d + 1
            held = bin(nm).count("1")
            if held > best[nc]:
                best[nc] = held
                queue.append((nc, nm, d + 1))
    return -1


def one_mark(grid, moves=MOVES):
    """One visited mark per cell, whichever arrival got there first, the mask carried along."""
    rows, cols, start, k = parse(grid)
    full = (1 << k) - 1
    if full == 0:
        return 0
    seen = [False] * (rows * cols)
    seen[start] = True
    queue = deque([(start, 0, 0)])
    while queue:
        cell, mask, d = queue.popleft()
        for nc, nm in step(grid, rows, cols, cell, mask, moves):
            if nm == full:
                return d + 1
            if not seen[nc]:
                seen[nc] = True
                queue.append((nc, nm, d + 1))
    return -1


def oracle(grid):
    """Layers of states with nothing marked visited, run for as many layers as there are states.

    Layer t is every (cell, mask) some walk of t moves stands on. A shortest
    walk to the full mask visits no state twice, so cells * 2^k layers are enough.
    """
    rows, cols, start, k = parse(grid)
    full = (1 << k) - 1
    if full == 0:
        return 0
    layer = {(start, 0)}
    for t in range(rows * cols << k):
        nxt = set()
        for cell, mask in layer:
            for nc, nm in step(grid, rows, cols, cell, mask):
                if nm == full:
                    return t + 1
                nxt.add((nc, nm))
        if not nxt:
            return -1
        layer = nxt
    return -1


class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        """BFS on (cell, mask) with a per-cell antichain of masks as the bar. The rest is in `__main__`."""
        return antichain_bar(grid)


def random_grid(rng, rows, cols, keys, wall):
    cells = [["#" if rng.random() < wall else "." for _ in range(cols)] for _ in range(rows)]
    spots = rng.sample(range(rows * cols), 1 + 2 * keys)
    for i, s in enumerate(spots):
        r, c = divmod(s, cols)
        cells[r][c] = "@" if i == 0 else chr(97 + (i - 1) // 2) if i % 2 else chr(65 + (i - 2) // 2)
    return ["".join(row) for row in cells]


def exhaustive(rows, cols, keys):
    """Every grid with '@', the keys and their locks on distinct cells and the rest '.' or '#'."""
    n = rows * cols
    marks = "@" + "".join(chr(97 + i) + chr(65 + i) for i in range(keys))
    for spots in itertools.permutations(range(n), len(marks)):
        rest = [i for i in range(n) if i not in spots]
        for walls in itertools.product(".#", repeat=len(rest)):
            cells = ["."] * n
            for s, m in zip(spots, marks):
                cells[s] = m
            for s, w in zip(rest, walls):
                cells[s] = w
            yield ["".join(cells[r * cols:(r + 1) * cols]) for r in range(rows)]


if __name__ == "__main__":
    rng = random.Random(864)
    started = time.time()
    orders = list(itertools.permutations(MOVES))

    for keys in (1, 2):
        print(f"== every 3x3 grid with {keys} key{'s' if keys > 1 else ''} and {keys} lock{'s' if keys > 1 else ''} ==")
        total = live = 0
        wrong = dict.fromkeys(["layered", "antichain bar", "count bar", "one mark"], 0)
        wrong_dead = dict.fromkeys(wrong, 0)
        by_order_mark = [0] * len(orders)
        by_order_count = [0] * len(orders)
        pops_l, pops_a = [0], [0]
        widest = [0]
        smallest = {}
        checked = 0
        for grid in exhaustive(3, 3, keys):
            total += 1
            want = layered(grid, pops_l)
            if keys == 1 or total % 7 == 0:
                checked += 1
                assert oracle(grid) == want, grid
            got = {
                "layered": want,
                "antichain bar": antichain_bar(grid, pops_a, widest),
                "count bar": count_bar(grid),
                "one mark": one_mark(grid),
            }
            if want == -1:
                for name in wrong:
                    wrong_dead[name] += got[name] != -1
                continue
            live += 1
            for name in wrong:
                if got[name] != want:
                    wrong[name] += 1
                    key = (sum(row.count("#") for row in grid), want)
                    if name not in smallest or key < smallest[name][0]:
                        smallest[name] = (key, grid, want, got[name])
            for i, order in enumerate(orders):
                by_order_mark[i] += one_mark(grid, order) != want
                by_order_count[i] += count_bar(grid, order) != want
        print(f"  grids {total}   answer exists {live} ({100 * live / total:.1f}%)   oracle agreed with layered on all {checked} checked")
        for name in wrong:
            print(f"  {name:14s} wrong {wrong[name]:6d}   {100 * wrong[name] / live:.2f}% of the answerable"
                  f"   and {wrong_dead[name]} of the {total - live} with no answer")
        for name, (key, grid, want, got) in smallest.items():
            print(f"    fewest walls for {name}: {' / '.join(grid)}: {want}, it says {got}")
        print(f"  one mark by the order the four moves are queued: best order wrong {min(by_order_mark)}"
              f" ({100 * min(by_order_mark) / live:.2f}%), worst {max(by_order_mark)} ({100 * max(by_order_mark) / live:.2f}%),"
              f" orders never wrong: {sum(1 for w in by_order_mark if w == 0)} of {len(orders)}")
        print(f"  count bar by order: best {min(by_order_count)} ({100 * min(by_order_count) / live:.2f}%),"
              f" worst {max(by_order_count)} ({100 * max(by_order_count) / live:.2f}%)")
        print(f"  pops: layered {pops_l[0]}   antichain bar {pops_a[0]}   saved {100 * (1 - pops_a[0] / pops_l[0]):.1f}%"
              f"   widest antichain at a cell {widest[0]} against the bound C({keys}, {keys // 2}) = "
              f"{len(list(itertools.combinations(range(keys), keys // 2)))}")

    print("\n== random grids, walls at 25% ==")
    print("  rows x cols  keys   grids  answerable   count bar   one mark   best order   antichain pops saved   widest   bound")
    for rows, cols, keys, count in ((4, 4, 2, 6000), (5, 5, 3, 4000), (6, 6, 4, 3000), (7, 7, 5, 1500), (8, 8, 6, 1000)):
        live = 0
        wrong = dict.fromkeys(["antichain bar", "count bar", "one mark"], 0)
        pops_l, pops_a, widest = [0], [0], [0]
        hist = {}
        sample = rng.sample(orders, 6)
        by_order = [0] * len(sample)
        for _ in range(count):
            grid = random_grid(rng, rows, cols, keys, 0.25)
            want = layered(grid, pops_l)
            w = [0]
            got = {"antichain bar": antichain_bar(grid, pops_a, w), "count bar": count_bar(grid), "one mark": one_mark(grid)}
            if want == -1:
                for name in wrong:
                    wrong[name] += got[name] != -1
                continue
            live += 1
            widest[0] = max(widest[0], w[0])
            hist[w[0]] = hist.get(w[0], 0) + 1
            for name in wrong:
                wrong[name] += got[name] != want
            for i, order in enumerate(sample):
                by_order[i] += one_mark(grid, order) != want
        bound = len(list(itertools.combinations(range(keys), keys // 2)))
        print(f"    {rows} x {cols}      {keys}    {count:5d}     {live:5d}      {wrong['count bar']:5d} ({100 * wrong['count bar'] / live:4.1f}%)"
              f"  {wrong['one mark']:5d} ({100 * wrong['one mark'] / live:4.1f}%)   {min(by_order):5d}"
              f"        {100 * (1 - pops_a[0] / pops_l[0]):5.1f}%              {widest[0]:2d}      {bound:2d}"
              f"   antichain bar wrong {wrong['antichain bar']}")
        print("           widest antichain per grid: " + "  ".join(f"{w}: {hist[w]}" for w in sorted(hist)))

    print("\n== the oracle on 3000 random 4x4 grids with 3 keys ==")
    bad = 0
    for _ in range(3000):
        grid = random_grid(rng, 4, 4, 3, 0.25)
        bad += oracle(grid) != layered(grid)
    print(f"  disagreements with layered: {bad}")

    print("\n== the statement's size: 30 x 30, 6 keys, walls at 20% ==")
    s = Solution()
    for seed in range(6):
        r = random.Random(seed)
        grid = random_grid(r, 30, 30, 6, 0.2)
        c1, c2, w = [0], [0], [0]
        t0 = time.time()
        a = layered(grid, c1)
        el1 = time.time() - t0
        t0 = time.time()
        b = antichain_bar(grid, c2, w)
        el2 = time.time() - t0
        assert a == b == s.shortestPathAllKeys(grid)
        print(f"  seed {seed}: answer {a:3d}   layered {c1[0]:6d} pops in {el1:.3f}s   antichain bar {c2[0]:6d} pops in {el2:.3f}s"
              f"   saved {100 * (1 - c2[0] / max(1, c1[0])):5.1f}%   widest {w[0]}   of {900 << 6} states")

    print(f"\n{time.time() - started:.0f}s")
