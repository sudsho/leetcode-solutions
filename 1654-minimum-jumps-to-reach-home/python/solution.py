import itertools
import random
import time
from collections import deque
from typing import List


def layered(forbidden, a, b, x, cap=None, counter=None):
    """BFS on (position, arrived by a backward jump), each of the two copies of a position visited once.

    `cap` is the furthest position the search may stand on. The default is
    max(x, max forbidden) + a + b.
    """
    if cap is None:
        cap = max([x] + list(forbidden)) + a + b
    blocked = [False] * (cap + 1)
    for f in forbidden:
        if f <= cap:
            blocked[f] = True
    seen = [[False, False] for _ in range(cap + 1)]
    seen[0][0] = True
    queue = deque([(0, 0, 0)])
    while queue:
        pos, back, jumps = queue.popleft()
        if counter is not None:
            counter[0] += 1
        if pos == x:
            return jumps
        nxt = pos + a
        if nxt <= cap and not blocked[nxt] and not seen[nxt][0]:
            seen[nxt][0] = True
            queue.append((nxt, 0, jumps + 1))
        nxt = pos - b
        if not back and nxt >= 0 and not blocked[nxt] and not seen[nxt][1]:
            seen[nxt][1] = True
            queue.append((nxt, 1, jumps + 1))
    return -1


def flag_bar(forbidden, a, b, x, cap=None, counter=None):
    """The same search with one bar per position: has an arrival that may still jump back been queued here.

    2093's bar with two values. An arrival by a forward jump can do everything
    an arrival by a backward jump can, and the queue is in jump order, so a
    backward arrival at a position a forward one already reached is dominated.
    The bar can be set at the push here because every jump costs 1.
    """
    if cap is None:
        cap = max([x] + list(forbidden)) + a + b
    blocked = [False] * (cap + 1)
    for f in forbidden:
        if f <= cap:
            blocked[f] = True
    free = [False] * (cap + 1)
    stuck = [False] * (cap + 1)
    free[0] = True
    queue = deque([(0, 0, 0)])
    while queue:
        pos, back, jumps = queue.popleft()
        if counter is not None:
            counter[0] += 1
        if pos == x:
            return jumps
        nxt = pos + a
        if nxt <= cap and not blocked[nxt] and not free[nxt]:
            free[nxt] = True
            queue.append((nxt, 0, jumps + 1))
        nxt = pos - b
        if not back and nxt >= 0 and not blocked[nxt] and not free[nxt] and not stuck[nxt]:
            stuck[nxt] = True
            queue.append((nxt, 1, jumps + 1))
    return -1


def one_mark(forbidden, a, b, x, back_first=False, cap=None):
    """BFS with one visited mark per position, whichever arrival got there first.

    The backward arrival cannot jump back again, so when it takes the mark the
    forward arrival that comes later is thrown away with the route it carried.
    """
    if cap is None:
        cap = max([x] + list(forbidden)) + a + b
    blocked = [False] * (cap + 1)
    for f in forbidden:
        if f <= cap:
            blocked[f] = True
    seen = [False] * (cap + 1)
    seen[0] = True
    queue = deque([(0, 0, 0)])
    while queue:
        pos, back, jumps = queue.popleft()
        if pos == x:
            return jumps
        moves = [(pos + a, 0)]
        if not back:
            moves.append((pos - b, 1))
        if back_first:
            moves.reverse()
        for nxt, flag in moves:
            if 0 <= nxt <= cap and not blocked[nxt] and not seen[nxt]:
                seen[nxt] = True
                queue.append((nxt, flag, jumps + 1))
    return -1


def mask_of(forbidden):
    m = 0
    for f in forbidden:
        m |= 1 << f
    return m


def oracle(fmask, a, b, x, cap):
    """Layers of positions as two bitsets, nothing visited, run for as many layers as there are states.

    Layer k is every (position, flag) some k jumps can stand on. No position
    is ever marked, so nothing here depends on a domination argument, and a
    shortest route to x visits no state twice, so 2 (cap + 1) layers are enough.
    """
    allowed = ((1 << (cap + 1)) - 1) & ~fmask
    free, stuck = 1, 0
    for jumps in range(2 * (cap + 1) + 1):
        if ((free | stuck) >> x) & 1:
            return jumps
        free, stuck = ((free | stuck) << a) & allowed, (free >> b) & allowed
        if not free and not stuck:
            return -1
    return -1


def bitset_bfs(fmask, a, b, x, cap):
    """The layered search on bitsets, with both visited sets. Fast enough to find the least cap that works."""
    allowed = ((1 << (cap + 1)) - 1) & ~fmask
    free, stuck = 1, 0
    seen_free, seen_stuck = 1, 0
    jumps = 0
    while free or stuck:
        if ((free | stuck) >> x) & 1:
            return jumps
        free, stuck = ((free | stuck) << a) & allowed & ~seen_free, (free >> b) & allowed & ~seen_stuck
        seen_free |= free
        seen_stuck |= stuck
        jumps += 1
    return -1


def least_cap(fmask, a, b, x, want, top):
    """The smallest cap at which the search returns `want`. The answer never gets worse with more room."""
    lo, hi = x, top
    while lo < hi:
        mid = (lo + hi) // 2
        if bitset_bfs(fmask, a, b, x, mid) == want:
            hi = mid
        else:
            lo = mid + 1
    return lo


class Solution:
    def minimumJumps(self, forbidden: List[int], a: int, b: int, x: int) -> int:
        """BFS on position with a can-still-jump-back bar. The rest is in `__main__`."""
        return flag_bar(forbidden, a, b, x)


if __name__ == "__main__":
    rng = random.Random(1654)
    started = time.time()
    TOP = 10
    CAP = 120

    caps = {
        "x + b": lambda f, a, b, x: x + b,
        "max(x, F) + b": lambda f, a, b, x: max([x] + f) + b,
        "max(x, F) + a": lambda f, a, b, x: max([x] + f) + a,
        "max(x, F) + a + b - 1": lambda f, a, b, x: max([x] + f) + a + b - 1,
        "max(x, F) + a + b": lambda f, a, b, x: max([x] + f) + a + b,
    }

    print(f"== every a, b in 1..6, x in 1..{TOP}, forbidden any subset of 1..{TOP} without x ==")
    total = live = 0
    wrong = dict.fromkeys(["layered", "flag bar", "one mark, forward first", "one mark, back first"], 0)
    wrong_cap = dict.fromkeys(caps, 0)
    wrong_cap_big_a = dict.fromkeys(caps, 0)
    live_big_a = 0
    excess_hist = {}
    worst = None
    pops_layered, pops_bar = [0], [0]
    smallest = {}
    for a, b, x in itertools.product(range(1, 7), range(1, 7), range(1, TOP + 1)):
        others = [p for p in range(1, TOP + 1) if p != x]
        for r in range(len(others) + 1):
            for f in itertools.combinations(others, r):
                f = list(f)
                fmask = mask_of(f)
                want = oracle(fmask, a, b, x, CAP)
                total += 1
                got = {
                    "layered": layered(f, a, b, x, counter=pops_layered),
                    "flag bar": flag_bar(f, a, b, x, counter=pops_bar),
                    "one mark, forward first": one_mark(f, a, b, x),
                    "one mark, back first": one_mark(f, a, b, x, back_first=True),
                }
                if want == -1:
                    for name in wrong:
                        wrong[name] += got[name] != -1
                    continue
                live += 1
                live_big_a += a >= b
                for name in wrong:
                    if got[name] != want:
                        wrong[name] += 1
                        key = (len(f), x)
                        if name.startswith("one mark") and (name not in smallest or key < smallest[name][0]):
                            smallest[name] = (key, (f, a, b, x, want, got[name]))
                for name, cap_of in caps.items():
                    bad = bitset_bfs(fmask, a, b, x, cap_of(f, a, b, x)) != want
                    wrong_cap[name] += bad
                    wrong_cap_big_a[name] += bad and a >= b
                need = least_cap(fmask, a, b, x, want, CAP)
                over = need - max([x] + f)
                excess_hist[over] = excess_hist.get(over, 0) + 1
                room = a + b - over
                if worst is None or room < worst[0]:
                    worst = (room, (f, a, b, x, want, need))
    print(f"  instances {total}   answer exists {live} ({100 * live / total:.1f}%)   with a >= b {live_big_a}")
    for name, k in wrong.items():
        print(f"  {name:26s} wrong {k:6d}   {100 * k / live:.2f}% of the answerable")
    for name, (key, inst) in smallest.items():
        f, a, b, x, want, got = inst
        print(f"    fewest forbidden: forbidden {f} a {a} b {b} x {x}: {want}, it says {got}")
    print("  the cap, wrong answers by where the search is cut off:")
    for name in caps:
        print(f"    {name:24s} wrong {wrong_cap[name]:6d}   {100 * wrong_cap[name] / live:.2f}%"
              f"     with a >= b {wrong_cap_big_a[name]:6d}")
    print("  least cap that still gives the answer, as positions past max(x, F):")
    for over in sorted(excess_hist):
        print(f"    {over:+3d}: {excess_hist[over]:7d}   {100 * excess_hist[over] / live:.2f}%")
    f, a, b, x, want, need = worst[1]
    print(f"  closest to the bound: a + b - excess = {worst[0]}, forbidden {f} a {a} b {b} x {x},"
          f" {want} jumps, needs cap {need}")
    print(f"  states popped: layered {pops_layered[0]}   flag bar {pops_bar[0]}"
          f"   saved {100 * (1 - pops_bar[0] / pops_layered[0]):.1f}%")

    print("\n== the oracle's own cap: 120 against 400 on 20000 random instances from the same ranges ==")
    moved = 0
    for _ in range(20000):
        a, b, x = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, TOP)
        f = [p for p in range(1, TOP + 1) if p != x and rng.random() < 0.5]
        moved += oracle(mask_of(f), a, b, x, 120) != oracle(mask_of(f), a, b, x, 400)
    print(f"  answers that move: {moved}")

    print("\n== random instances, forbidden past x allowed ==")
    for top_ab, top_x, top_f, count_f, count in ((8, 30, 40, 10, 20000), (12, 40, 60, 25, 20000),
                                                 (20, 100, 150, 60, 10000), (50, 300, 400, 100, 5000)):
        live = 0
        wrong = dict.fromkeys(["layered", "flag bar", "one mark, forward first", "one mark, back first"], 0)
        wrong_cap = dict.fromkeys(caps, 0)
        least_room = None
        for _ in range(count):
            a, b, x = rng.randint(1, top_ab), rng.randint(1, top_ab), rng.randint(1, top_x)
            f = sorted(set(rng.randint(1, top_f) for _ in range(count_f)) - {x})
            fmask = mask_of(f)
            big = 4 * (max([x] + f) + a + b) + 200
            want = oracle(fmask, a, b, x, big)
            got = {
                "layered": layered(f, a, b, x),
                "flag bar": flag_bar(f, a, b, x),
                "one mark, forward first": one_mark(f, a, b, x),
                "one mark, back first": one_mark(f, a, b, x, back_first=True),
            }
            if want == -1:
                for name in wrong:
                    wrong[name] += got[name] != -1
                continue
            live += 1
            for name in wrong:
                wrong[name] += got[name] != want
            for name, cap_of in caps.items():
                wrong_cap[name] += bitset_bfs(fmask, a, b, x, cap_of(f, a, b, x)) != want
            room = a + b - (least_cap(fmask, a, b, x, want, big) - max([x] + f))
            least_room = room if least_room is None else min(least_room, room)
        print(f"  a, b <= {top_ab:2d} x <= {top_x:3d} forbidden {count_f:3d} in 1..{top_f:3d}  instances {count}"
              f"  answerable {live}")
        print("    " + "   ".join(f"{n} {k}" for n, k in wrong.items()))
        print("    cap: " + "   ".join(f"{n}: {k}" for n, k in wrong_cap.items())
              + f"   least a + b - excess {least_room}")

    print("\n== how far past max(x, F): every a < b <= 8, x in 1..16, at most 2 forbidden in 1..16 ==")
    reached, short, cut_wrong, cut_live = [], [], 0, 0
    for a, b in itertools.combinations(range(1, 9), 2):
        most = None
        for x in range(1, 17):
            others = [p for p in range(1, 17) if p != x]
            for r in range(3):
                for f in itertools.combinations(others, r):
                    fmask = mask_of(f)
                    want = oracle(fmask, a, b, x, 200)
                    if want == -1:
                        continue
                    cut_live += 1
                    top = max((x,) + f)
                    cut_wrong += bitset_bfs(fmask, a, b, x, top + a + b - 1) != want
                    over = least_cap(fmask, a, b, x, want, 200) - top
                    if most is None or over > most[0]:
                        most = (over, list(f), x, want)
        (reached if most[0] == a + b else short).append((a, b, most))
    print(f"  answerable {cut_live}   wrong with the cap one short, max(x, F) + a + b - 1: {cut_wrong}")
    print(f"  pairs that need all of a + b: {len(reached)} of {len(reached) + len(short)}")
    for a, b, (over, f, x, want) in reached:
        print(f"    a {a} b {b}: forbidden {f} x {x}, {want} jumps, stands on {max([x] + f) + over}")
    print("  the rest, most needed against a + b: "
          + "  ".join(f"({a},{b}) {m[0]}/{a + b}" for a, b, m in short))

    print("\n== one mark with the backward jump queued first, 300000 random instances, a, b <= 14 ==")
    live = bad = bad_fwd = 0
    for _ in range(300000):
        a, b, x = rng.randint(1, 14), rng.randint(1, 14), rng.randint(1, 40)
        f = sorted(set(rng.randint(1, 50) for _ in range(rng.randint(0, 20))) - {x})
        want = bitset_bfs(mask_of(f), a, b, x, max([x] + f) + a + b)
        if want == -1:
            continue
        live += 1
        bad += one_mark(f, a, b, x, back_first=True) != want
        bad_fwd += one_mark(f, a, b, x) != want
    print(f"  answerable {live}   back first wrong {bad}   forward first wrong {bad_fwd}"
          f" ({100 * bad_fwd / live:.1f}%)")

    print("\n== the statement's size: a, b, x <= 2000, forbidden <= 1000 positions <= 2000 ==")
    s = Solution()
    for a, b, x, count_f in ((1998, 1999, 2000, 0), (1999, 1998, 1, 1000), (2, 1, 2000, 1000), (1, 2000, 1999, 1000),
                             (29, 98, 80, 4), (1000, 999, 1, 500), (3, 2000, 1999, 900)):
        f = sorted(set(rng.randint(1, 2000) for _ in range(count_f)) - {x})
        t0 = time.time()
        ans = s.minimumJumps(f, a, b, x)
        el = time.time() - t0
        t0 = time.time()
        ref = layered(f, a, b, x, cap=6000)
        el6 = time.time() - t0
        c1, c2 = [0], [0]
        layered(f, a, b, x, counter=c1)
        flag_bar(f, a, b, x, counter=c2)
        far = oracle(mask_of(f), a, b, x, 40000)
        print(f"  a {a:4d} b {b:4d} x {x:4d} forbidden {len(f):4d}   answer {ans} in {el:.4f}s"
              f"   cap 6000 {ref} in {el6:.4f}s   cap 40000 {far}   popped {c1[0]} layered, {c2[0]} with the bar")

    print(f"\n{time.time() - started:.0f}s")
