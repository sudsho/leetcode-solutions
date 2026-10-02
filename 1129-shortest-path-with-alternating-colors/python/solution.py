import itertools
import random
import time
from collections import deque
from typing import List

RED, BLUE = 0, 1


def adjacency(n, red, blue):
    """adj[c][u] lists the heads of u's edges of colour c, in input order."""
    adj = [[[] for _ in range(n)] for _ in range(2)]
    for c, edges in ((RED, red), (BLUE, blue)):
        for u, v in edges:
            adj[c][u].append(v)
    return adj


def layered(n, red, blue, counter=None, first=RED):
    """BFS on (node, colour of the edge that arrived), each state queued once. The textbook search.

    (0, RED) and (0, BLUE) are both at level 0, so the first edge out of 0 can
    be either colour. A state arrived by colour c leaves by colour 1 - c.
    """
    adj = adjacency(n, red, blue)
    ans = [-1] * n
    ans[0] = 0
    seen = [[False] * n for _ in range(2)]
    queue = deque()
    for c in (first, 1 - first):
        seen[c][0] = True
        queue.append((0, c, 0))
    while queue:
        u, c, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        for w in adj[1 - c][u]:
            if not seen[1 - c][w]:
                seen[1 - c][w] = True
                if ans[w] < 0:
                    ans[w] = d + 1
                queue.append((w, 1 - c, d + 1))
    return ans


def pruned(n, red, blue, counter=None):
    """layered with the states that cannot move never queued.

    A state arrived by c at w can only leave by 1 - c. If w has no edge of
    colour 1 - c the state still answers w but has nowhere to go, so it is
    recorded and not pushed. At a node whose out-edges are one colour that
    leaves one live state, and the bar there is one mark, which is the only
    sense in which the colour coordinate is ordered on this problem: at w,
    the arrival that can still move dominates the one that cannot.
    """
    adj = adjacency(n, red, blue)
    ans = [-1] * n
    ans[0] = 0
    seen = [[False] * n for _ in range(2)]
    queue = deque()
    for c in (RED, BLUE):
        seen[c][0] = True
        if adj[1 - c][0]:
            queue.append((0, c, 0))
    while queue:
        u, c, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        nc = 1 - c
        for w in adj[nc][u]:
            if not seen[nc][w]:
                seen[nc][w] = True
                if ans[w] < 0:
                    ans[w] = d + 1
                if adj[c][w]:
                    queue.append((w, nc, d + 1))
    return ans


def one_mark(n, red, blue, first=RED):
    """One mark per node, whichever colour arrives first. Reads the colour as if it did not matter."""
    adj = adjacency(n, red, blue)
    ans = [-1] * n
    ans[0] = 0
    seen = [False] * n
    seen[0] = True
    queue = deque([(0, first, 0), (0, 1 - first, 0)])
    while queue:
        u, c, d = queue.popleft()
        for w in adj[1 - c][u]:
            if not seen[w]:
                seen[w] = True
                ans[w] = d + 1
                queue.append((w, 1 - c, d + 1))
    return ans


def mono_mark(n, red, blue, first=RED):
    """One mark at nodes whose out-edges are one colour, two marks elsewhere, and nothing pruned.

    The bar `pruned` uses, without the pruning. At a one-colour node only one
    arrival colour can move on, and this keeps whichever arrives first, so it
    is right exactly when the dead arrival never beats the live one there.
    """
    adj = adjacency(n, red, blue)
    mono = [not (adj[RED][u] and adj[BLUE][u]) for u in range(n)]
    ans = [-1] * n
    ans[0] = 0
    seen = [[False] * n for _ in range(2)]
    queue = deque()
    for c in (first, 1 - first):
        seen[c][0] = True
        queue.append((0, c, 0))
    if mono[0]:
        seen[0][0] = seen[1][0] = True
    while queue:
        u, c, d = queue.popleft()
        nc = 1 - c
        for w in adj[nc][u]:
            if not seen[nc][w]:
                seen[nc][w] = True
                if mono[w]:
                    seen[c][w] = True
                if ans[w] < 0:
                    ans[w] = d + 1
                queue.append((w, nc, d + 1))
    return ans


def oracle(n, red, blue):
    """Every layer as a set of states, nothing marked, 2n layers. There are 2n states, so a shortest walk is shorter."""
    adj = adjacency(n, red, blue)
    ans = [-1] * n
    ans[0] = 0
    layer = {(0, RED), (0, BLUE)}
    for d in range(1, 2 * n + 1):
        layer = {(w, 1 - c) for u, c in layer for w in adj[1 - c][u]}
        for w, _ in layer:
            if ans[w] < 0:
                ans[w] = d
    return ans


class Solution:
    def shortestAlternatingPaths(
        self, n: int, redEdges: List[List[int]], blueEdges: List[List[int]]
    ) -> List[int]:
        """BFS on (node, arriving colour), with the states that cannot move recorded and not queued. The rest is in `__main__`."""
        return pruned(n, redEdges, blueEdges)


def exhaustive(n):
    """Every pair of edge sets on n labelled nodes, self-loops allowed, one edge per (u, v, colour)."""
    pairs = [(u, v) for u in range(n) for v in range(n)]
    k = len(pairs)
    for bits in range(1 << (2 * k)):
        red = [pairs[i] for i in range(k) if bits >> i & 1]
        blue = [pairs[i] for i in range(k) if bits >> (k + i) & 1]
        yield red, blue


def random_instance(rng, n, m):
    pairs = [(u, v) for u in range(n) for v in range(n)]
    chosen = rng.sample([(c, p) for c in (RED, BLUE) for p in pairs], m)
    return [p for c, p in chosen if c == RED], [p for c, p in chosen if c == BLUE]


if __name__ == "__main__":
    s = Solution()
    print(s.shortestAlternatingPaths(3, [[0, 1], [1, 2]], []), "expect [0, 1, -1]")
    print(s.shortestAlternatingPaths(3, [[0, 1]], [[2, 1]]), "expect [0, 1, -1]")

    t0 = time.time()
    print("\nexhaustive, against the layer oracle")
    for n in (2, 3):
        total = 0
        bad = {"layered": 0, "pruned": 0, "one_mark R": 0, "one_mark B": 0, "mono R": 0, "mono B": 0}
        wrong_sets = {"one_mark R": set(), "one_mark B": set()}
        smallest = None
        for idx, (red, blue) in enumerate(exhaustive(n)):
            total += 1
            want = oracle(n, red, blue)
            got = {
                "layered": layered(n, red, blue),
                "pruned": pruned(n, red, blue),
                "one_mark R": one_mark(n, red, blue, RED),
                "one_mark B": one_mark(n, red, blue, BLUE),
                "mono R": mono_mark(n, red, blue, RED),
                "mono B": mono_mark(n, red, blue, BLUE),
            }
            for k, v in got.items():
                if v != want:
                    bad[k] += 1
                    if k in wrong_sets:
                        wrong_sets[k].add(idx)
            if got["one_mark R"] != want or got["one_mark B"] != want:
                m = len(red) + len(blue)
                if smallest is None or m < smallest[0]:
                    smallest = (m, red, blue, want, got["one_mark R"], got["one_mark B"])
        print(f"  n = {n}: {total} instances")
        for k, v in bad.items():
            print(f"    {k:11s} wrong on {v:6d}  {100 * v / total:.2f}%")
        a, b = wrong_sets["one_mark R"], wrong_sets["one_mark B"]
        print(f"    one_mark R and B wrong sets: |R| = {len(a)}, |B| = {len(b)}, both {len(a & b)}")
        if smallest:
            print(f"    fewest-edges one_mark failure: red {smallest[1]} blue {smallest[2]}"
                  f" want {smallest[3]} R-first {smallest[4]} B-first {smallest[5]}")

    print("\nn = 3 failures grouped by (node, true answer), and the edges every member agrees on")
    pairs = [(u, v) for u in range(3) for v in range(3)]
    names = ["r%d%d" % p for p in pairs] + ["b%d%d" % p for p in pairs]
    for name, first in (("one_mark B", BLUE), ("mono B", BLUE)):
        fn = one_mark if name.startswith("one") else mono_mark
        groups = {}
        for bits, (red, blue) in enumerate(exhaustive(3)):
            want, got = oracle(3, red, blue), fn(3, red, blue, first)
            if got != want:
                key = tuple((i, want[i]) for i in range(3) if got[i] != want[i])
                groups.setdefault(key, []).append(bits)
        for key, members in sorted(groups.items()):
            fixed = [names[i] + "=" + str(members[0] >> i & 1) for i in range(18)
                     if all((b >> i & 1) == (members[0] >> i & 1) for b in members)]
            print(f"  {name:10s} node, answer {key}: {len(members):5d}, fixed {' '.join(fixed)}")

    print("\nrandom, n = 6 and n = 10, 20000 each over edge counts")
    rng = random.Random(1129)
    for n in (6, 10):
        rows = []
        for m in (n, 2 * n, 4 * n, n * n):
            bad = {"layered": 0, "pruned": 0, "one_mark R": 0, "mono R": 0}
            pops_l = pops_p = 0
            reps = 5000
            for _ in range(reps):
                red, blue = random_instance(rng, n, m)
                want = oracle(n, red, blue)
                cl, cp = [0], [0]
                if layered(n, red, blue, cl) != want:
                    bad["layered"] += 1
                if pruned(n, red, blue, cp) != want:
                    bad["pruned"] += 1
                if one_mark(n, red, blue) != want:
                    bad["one_mark R"] += 1
                if mono_mark(n, red, blue) != want:
                    bad["mono R"] += 1
                pops_l += cl[0]
                pops_p += cp[0]
            print(f"  n = {n:2d} m = {m:3d}: " + " ".join(f"{k}={100 * v / reps:.2f}%" for k, v in bad.items())
                  + f"  pruned saves {100 * (1 - pops_p / pops_l):.1f}% of pops")

    print("\nhow the wrong readings are wrong, 4000 random instances at each (n, m)")
    rng = random.Random(5)
    for name, fn in (("one_mark", one_mark), ("mono", mono_mark)):
        neg = long = short = 0
        for n in (4, 6, 10):
            for m in (n, 2 * n, 4 * n):
                for _ in range(4000):
                    red, blue = random_instance(rng, n, m)
                    for g, w in zip(fn(n, red, blue), oracle(n, red, blue)):
                        if g != w:
                            neg += g == -1
                            long += g > w >= 0
                            short += 0 <= g < w
        print(f"  {name:8s} nodes said -1 {neg}, too long {long}, too short {short}")

    print("\ntime at n = 100, 400 edges, 2000 instances")
    rng = random.Random(7)
    insts = [random_instance(rng, 100, 400) for _ in range(2000)]
    for name, fn in (("layered", layered), ("pruned", pruned)):
        t = time.time()
        for red, blue in insts:
            fn(100, red, blue)
        print(f"  {name:8s} {1000 * (time.time() - t) / len(insts):.3f} ms each")

    print(f"\n{time.time() - t0:.0f} s")
