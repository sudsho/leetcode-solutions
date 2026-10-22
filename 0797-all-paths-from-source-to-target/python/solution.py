"""797. All Paths From Source to Target.

Every path from 0 to n - 1 in a DAG, by dfs with one path on the stack. The
problem is here as an instrument: 1786 asked how many restricted paths a
graph of n nodes can hold and left it at "layers of three would grow like
3^(n/3)". A restricted path is a path in the DAG the distance potential
defines, and every DAG whose nodes all reach the sink is a 1786 instance
with weight = fall in potential, so 1786's maximum is the most paths a DAG
on n nodes and m edges can hold, which is this problem's output size.

Run as a script: the realisation check against 1786's own program, the
exhaustive maximum over DAGs to n = 9 by predecessor sets, chains of
complete blocks against it, a climber at n = 13, and the best chain at
1786's statement size, n = 20000 and m = 40000, through 1786's program.
Section 5 (Oct 20) frees the node count and asks the most paths for m
edges alone, over strips to m = 44 and the exhaustive table where it reaches.
Section 6 (Oct 22) rewrites any DAG into a strip that is never worse, which
makes the strip the maximum at every n and m.
"""

import importlib.util
import os
import random
import time
from typing import List

MOD = 10 ** 9 + 7
HERE = os.path.dirname(os.path.abspath(__file__))
P1786 = os.path.join(HERE, "..", "..", "1786-number-of-restricted-paths-from-first-to-last-node",
                     "python", "solution.py")


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)
        out, path = [], [0]

        def go(u):
            if u == n - 1:
                out.append(path[:])
                return
            for v in graph[u]:
                path.append(v)
                go(v)
                path.pop()

        go(0)
        return out


# ---------------------------------------------------------------- counting

def count_paths(n, preds):
    """Paths from 0 to n - 1 when preds[j] is the bitmask of j's predecessors, all below j."""
    c = [0] * n
    c[0] = 1
    for j in range(1, n):
        s, p = 0, preds[j]
        while p:
            low = p & -p
            s += c[low.bit_length() - 1]
            p ^= low
        c[j] = s
    return c[n - 1]


def pairs(n):
    return [(i, j) for j in range(n) for i in range(j)]


def preds_of(n, pr, mask):
    preds = [0] * n
    for b, (i, j) in enumerate(pr):
        if mask >> b & 1:
            preds[j] |= 1 << i
    return preds


def full_enumeration(n):
    """Most paths at each exact edge count over every DAG on 0..n-1 in index order, with a witness."""
    pr = pairs(n)
    best = {}
    for mask in range(1 << len(pr)):
        preds = preds_of(n, pr, mask)
        c = count_paths(n, preds)
        m = bin(mask).count("1")
        if c > best.get(m, (-1, 0))[0]:
            best[m] = (c, mask)
    return best


def subset_sums(values):
    k = len(values)
    sums = [0] * (1 << k)
    for s in range(1, 1 << k):
        low = s & -s
        sums[s] = sums[s ^ low] + values[low.bit_length() - 1]
    return sums


def exhaustive(n):
    """Most paths with at most m edges on at most n nodes, for every m.

    The predecessor sets of nodes 1..n-4 are enumerated outright. The last
    three nodes q < p < t draw the rest of their predecessors from the base
    0..n-4, and t's count is a sum of the base subset sums of q, p and t
    with q's and p's counts added where the three are joined, every term
    non-negative, so each set only needs its best value per size.
    """
    base = n - 3
    pop = [bin(s).count("1") for s in range(1 << base)]
    top = n * (n - 1) // 2
    best = [0] * (top + 1)
    counts = [1]

    def close(m0):
        sums = subset_sums(counts)
        bb = [0] * (base + 1)
        for s, v in enumerate(sums):
            if v > bb[pop[s]]:
                bb[pop[s]] = v
        for c in range(base + 1):
            if bb[c] > best[m0 + c]:                 # t from the base alone
                best[m0 + c] = bb[c]
            for a in range(base + 1):
                v = bb[a] + bb[c]                     # t from the base and one of q, p
                if v > best[m0 + a + c + 1]:
                    best[m0 + a + c + 1] = v
                for b in range(base + 1):
                    v = bb[a] + bb[b] + bb[c]         # t <- p <- q, or t <- q and t <- p
                    if v > best[m0 + a + b + c + 2]:
                        best[m0 + a + b + c + 2] = v
                    v += bb[a]                        # t <- q, t <- p and p <- q
                    if v > best[m0 + a + b + c + 3]:
                        best[m0 + a + b + c + 3] = v

    def rec(j, m0):
        if j == base:
            close(m0)
            return
        sums = subset_sums(counts)
        for s in range(1 << j):
            counts.append(sums[s])
            rec(j + 1, m0 + pop[s])
            counts.pop()

    rec(1, 0)
    for m in range(1, top + 1):
        best[m] = max(best[m], best[m - 1])
    return best


def chain_best(n, m):
    """log2 of the most paths a chain of complete blocks holds on at most n nodes and m edges, and the blocks."""
    f = [[-1] * (m + 1) for _ in range(n + 1)]
    how = [[None] * (m + 1) for _ in range(n + 1)]
    f[1][0] = 0
    for v in range(1, n + 1):
        for e in range(m + 1):
            if f[v][e] < 0:
                continue
            k = 2
            while v + k - 1 <= n and e + k * (k - 1) // 2 <= m:
                nv, ne = v + k - 1, e + k * (k - 1) // 2
                if f[v][e] + k - 2 > f[nv][ne]:
                    f[nv][ne] = f[v][e] + k - 2
                    how[nv][ne] = (v, e, k)
                k += 1
    bv, be = 1, 0
    for v in range(1, n + 1):
        for e in range(m + 1):
            if f[v][e] > f[bv][be]:
                bv, be = v, e
    blocks = []
    v, e = bv, be
    while how[v][e]:
        v, e, k = how[v][e]
        blocks.append(k)
    return f[bv][be], blocks[::-1]


# -------------------------------------------------------------- 1786 side

def load_1786():
    spec = importlib.util.spec_from_file_location("p1786", P1786)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution()


def all_reach_sink(n, preds):
    succ = [0] * n
    for j in range(n):
        p = preds[j]
        while p:
            low = p & -p
            succ[low.bit_length() - 1] |= 1 << j
            p ^= low
    ok = 1 << (n - 1)
    for j in range(n - 2, -1, -1):
        if succ[j] & ok:
            ok |= 1 << j
    return ok == (1 << n) - 1


def instance(n, preds, potential):
    """The 1786 instance of a DAG: nodes 1..n, weight = fall in a potential strictly decreasing along edges."""
    edges = []
    for j in range(n):
        p = preds[j]
        while p:
            low = p & -p
            i = low.bit_length() - 1
            p ^= low
            edges.append([i + 1, j + 1, potential[i] - potential[j]])
    return edges


def chain_preds(blocks):
    """A chain of complete blocks, block sizes in order, sharing one node between neighbours."""
    n = 1 + sum(k - 1 for k in blocks)
    preds = [0] * n
    start = 0
    for k in blocks:
        for j in range(start + 1, start + k):
            for i in range(start, j):
                preds[j] |= 1 << i
        start += k - 1
    return n, preds


def layered_preds(width, layers):
    """A source, `layers` layers of `width` nodes fully joined to the next, a sink: 1786's ladder at width 2."""
    n = 2 + width * layers
    preds = [0] * n
    for k in range(layers):
        lo = 1 + width * k
        prev = [0] if k == 0 else list(range(lo - width, lo))
        for j in range(lo, lo + width):
            for i in prev:
                preds[j] |= 1 << i
    for i in range(n - 1 - width, n - 1):
        preds[n - 1] |= 1 << i
    return n, preds


def climb(rng, n, m, steps, restarts):
    """Swap one edge for another, keep the change when the count does not fall; the best seen."""
    pr = pairs(n)
    found = 0
    for _ in range(restarts):
        chosen = rng.sample(range(len(pr)), m)
        inset = set(chosen)
        preds = preds_of(n, pr, sum(1 << b for b in chosen))
        cur = count_paths(n, preds)
        for _ in range(steps):
            k = rng.randrange(m)
            new = rng.randrange(len(pr))
            if new in inset:
                continue
            i, j = pr[chosen[k]]
            preds[j] ^= 1 << i
            i2, j2 = pr[new]
            preds[j2] |= 1 << i2
            c = count_paths(n, preds)
            if c >= cur:
                cur = c
                inset.remove(chosen[k])
                inset.add(new)
                chosen[k] = new
            else:
                preds[j2] ^= 1 << i2
                preds[j] |= 1 << i
        found = max(found, cur)
    return found


def window_best(n, m, cap=None):
    """Most paths when every node's predecessors are the k nodes just before it, over every
    in-degree sequence with at most m edges and k at most cap; a strip of windows."""
    best = [0] * (m + 1)
    counts = [1]

    def rec(j, used):
        if j == n:
            if counts[-1] > best[used]:
                best[used] = counts[-1]
            return
        for k in range(1, min(j, cap or j) + 1):
            if used + k > m:
                break
            counts.append(sum(counts[j - k:j]))
            rec(j + 1, used + k)
            counts.pop()

    rec(1, 0)
    for e in range(1, m + 1):
        best[e] = max(best[e], best[e - 1])
    return best


def strip_free(m, kmin=2, kmax=5):
    """Most paths over strips with at most m edges and the node count free, with the in-degree
    sequence that reaches it. Node 1 has one predecessor whatever kmin says, since it has one
    node before it; every later node takes between kmin and kmax of the nodes just before it."""
    best = [0] * (m + 1)
    how = [None] * (m + 1)
    counts, seq = [1], []

    def rec(j, used):
        if j >= 2 and counts[-1] > best[used]:
            best[used] = counts[-1]
            how[used] = tuple(seq)
        for k in range(1 if j == 1 else kmin, min(j, kmax) + 1):
            if used + k > m:
                break
            counts.append(sum(counts[j - k:j]))
            seq.append(k)
            rec(j + 1, used + k)
            counts.pop()
            seq.pop()

    rec(1, 0)
    for e in range(1, m + 1):
        if best[e - 1] > best[e]:
            best[e], how[e] = best[e - 1], how[e - 1]
    return best, how


def strip_preds(n, widths):
    """A strip: node j takes the widths[j] nodes before it (1 where widths runs out, at most j)."""
    preds = [0] * n
    for j in range(1, n):
        k = min(j, widths.get(j, 2))
        for i in range(j - k, j):
            preds[j] |= 1 << i
    return preds


def top_rewrite(n, preds):
    """Give each node, in index order, as many predecessors as it had, taken from the earlier
    nodes with the largest new counts. Returns the in-degrees of the nonzero nodes in order and
    the largest new count. Every new count dominates (section 6), so this is never below the
    old count at n - 1, and the result is a strip on at most n nodes with the same edges."""
    new, widths = [1], []
    for j in range(1, n):
        k = bin(preds[j]).count("1")
        if k == 0:
            continue
        new.append(sum(sorted(new, reverse=True)[:k]))
        widths.append(k)
    return widths, max(new)


def strip_any(m, floor, budget):
    """Strips with any in-degree on at most m edges, nodes free, pruned against `floor` (the
    in-degree 2 to 5 maximum per edge count): a node taking k nodes is at most k times the
    last count, so a branch at count t with r edges left reaches at most t * prod(r), the
    largest product of parts summing to r, and is dropped when that cannot beat floor
    anywhere. Returns the cells where something beat floor and whether it finished in budget."""
    prod = [1] * (m + 1)
    for r in range(2, m + 1):
        prod[r] = max(k * prod[r - k] for k in range(1, r + 1))
    thr = [min(floor[e] // prod[e - u] for e in range(u, m + 1)) for u in range(m + 1)]
    beat, counts, stop = {}, [1], time.time() + budget

    def rec(j, used):
        if time.time() > stop:
            return False
        t = counts[-1]
        if j >= 2 and t > floor[used]:
            beat[used] = max(beat.get(used, 0), t)
        if t <= thr[used]:
            return True
        for k in range(1, min(j, m - used) + 1):
            counts.append(sum(counts[j - k:j]))
            done = rec(j + 1, used + k)
            counts.pop()
            if not done:
                return False
        return True

    return beat, rec(1, 0)


def digits(x):
    return len(str(x))


def main():
    t0 = time.time()
    rng = random.Random(797)
    p1786 = load_1786()

    print("797, all paths from source to target, as the instrument for 1786's maximum\n")

    # 1. every DAG whose nodes all reach the sink is a 1786 instance with the same count
    print("1. realisation: the DAG's path count against 1786's program on weight = fall in potential")
    for n in (3, 4, 5):
        pr = pairs(n)
        tried = agree = 0
        for mask in range(1 << len(pr)):
            preds = preds_of(n, pr, mask)
            if not all_reach_sink(n, preds):
                continue
            tried += 1
            want = count_paths(n, preds) % MOD
            got = p1786.countRestrictedPaths(n, instance(n, preds, [n - 1 - i for i in range(n)]))
            agree += want == got
        print(f"  n = {n}: {agree} of {tried} DAGs with every node reaching the sink agree, "
              f"of {1 << len(pr)} edge sets")
        assert agree == tried
    n, tried, agree = 9, 0, 0
    pr = pairs(n)
    while tried < 2000:
        mask = sum(1 << b for b in range(len(pr)) if rng.random() < 0.4)
        preds = preds_of(n, pr, mask)
        if not all_reach_sink(n, preds):
            continue
        tried += 1
        pot = sorted(rng.sample(range(1, 10 ** 6), n - 1), reverse=True) + [0]
        want = count_paths(n, preds) % MOD
        agree += want == p1786.countRestrictedPaths(n, instance(n, preds, pot))
    print(f"  n = 9: {agree} of {tried} random DAGs agree under random potentials")
    assert agree == tried

    # 2. the exhaustive maximum per (n, m) and the chain of complete blocks against it
    print("\n2. most paths on at most n nodes and at most m edges, exhaustive (chain of complete blocks)")
    for n in (4, 5, 6):
        full = full_enumeration(n)
        fast = exhaustive(n)
        run = 0
        for m in range(1, n * (n - 1) // 2 + 1):
            run = max(run, full.get(m, (0, 0))[0])
            assert run == fast[m], (n, m, run, fast[m])
    print("  the predecessor-set enumeration matches the plain one at n = 4, 5, 6")
    beaten = cells = flat_total = 0
    worst = (1.0, None)
    table = {}
    for n in range(4, 10):
        ex = exhaustive(n)
        top = n * (n - 1) // 2
        row = []
        flats = 0
        for m in range(n - 1, top + 1):
            ch, blocks = chain_best(n, m)
            chv = 1 << ch
            mark = ""
            if n - 1 < m < top:
                cells += 1
                if ex[m] > chv:
                    beaten += 1
                    mark = "*"
                    if ex[m] / chv > worst[0]:
                        worst = (ex[m] / chv, (n, m, ex[m], chv))
            if m > n - 1 and ex[m] == ex[m - 1]:
                flats += 1
            row.append(f"{m}:{ex[m]}({chv}){mark}")
            table[(n, m)] = (ex[m], chv, blocks)
        flat_total += flats
        print(f"  n = {n}, {flats} flat steps, {time.time() - t0:.0f} s")
        print("    " + " ".join(row))
    print(f"  chain beaten on {beaten} of {cells} cells with n - 1 < m < C(n, 2), "
          f"worst {worst[0]:.3f}x at n, m, exhaustive, chain = {worst[1]}; {flat_total} flat steps in all")
    print(f"  (7, 9) = {table[(7, 9)][0]} chain {table[(7, 9)][1]} {table[(7, 9)][2]}; "
          f"(7, 12) = {table[(7, 12)][0]} chain {table[(7, 12)][1]} {table[(7, 12)][2]}; "
          f"(9, 20) = {table[(9, 20)][0]} chain {table[(9, 20)][1]} {table[(9, 20)][2]}")
    print("  witnesses at n = 5 and 6 where the chain is beaten:")
    for n in (5, 6):
        full = full_enumeration(n)
        pr = pairs(n)
        for m in sorted(full):
            ch, _ = chain_best(n, m)
            c, mask = full[m]
            if c > (1 << ch) and n - 1 < m < n * (n - 1) // 2:
                edges = [pr[b] for b in range(len(pr)) if mask >> b & 1]
                print(f"    n = {n}, m = {m}: {c} against {1 << ch}  {edges}")

    # 2b. after the table: the maximisers read as strips, each node joined to the nodes just before it
    print("\n2b. strips of windows against the exhaustive table")
    for n in range(4, 10):
        ex = exhaustive(n)
        top = n * (n - 1) // 2
        wb = [max(col) for col in zip(*(window_best(k, top) for k in range(2, n + 1)))]
        short = [m for m in range(n - 1, top + 1) if wb[m] < ex[m]]
        over = [m for m in range(n - 1, top + 1) if wb[m] > ex[m]]
        assert not over, (n, over)
        print(f"  n = {n}: strips on at most n nodes match the exhaustive maximum on "
              f"{top - n + 2 - len(short)} of {top - n + 2} cells" + (f", short at m = {short}" if short else ""))
    strip = [1, 1]
    while len(strip) < 10:
        strip.append(strip[-1] + strip[-2])
    print(f"  the fibonacci strip, each node on the two before it, 2n - 3 edges: "
          f"{' '.join(f'({n}, {2 * n - 3}) = {strip[n - 1]}' for n in range(5, 10))}")

    # 3. the climber at n = 13
    print("\n3. the climber at n = 13, 20 restarts of 3000 swaps, against the chain and the strips")
    wb = window_best(13, 30, cap=3)
    for m in (24, 30):
        ch, blocks = chain_best(13, m)
        found = climb(rng, 13, m, 3000, 20)
        print(f"  m = {m}: climber {found}, chain {1 << ch} {blocks}, strips with windows to 3: {wb[m]}")
    fibs = count_paths(13, strip_preds(13, {}))
    k4s = count_paths(13, strip_preds(13, {3: 3}))
    print(f"  the fibonacci strip at (13, 23) = {fibs}, with a K4 start at (13, 24) = {k4s}")

    # 4. the statement's size
    print("\n4. at 1786's size, n <= 20000 and m <= 40000")
    N, M = 20000, 40000
    best = (0, None)
    for y5 in range(0, 4001):
        for y3 in range(0, 3):
            nodes, edges = 4 * y5 + 2 * y3, 10 * y5 + 3 * y3
            if nodes + 1 > N or edges > M:
                continue
            x4 = min((N - 1 - nodes) // 3, (M - edges) // 6)
            e = y3 + 2 * x4 + 3 * y5
            if e > best[0]:
                best = (e, (y3, x4, y5))
    e, (y3, x4, y5) = best
    print(f"  best chain of K3, K4, K5 blocks: {y3} K3, {x4} K4, {y5} K5, 2^{e}, {digits(2 ** e)} digits, "
          f"n = {1 + 2 * y3 + 3 * x4 + 4 * y5}, m = {3 * y3 + 6 * x4 + 10 * y5}")
    n, preds = chain_preds([3] * y3 + [4] * x4 + [5] * y5)
    exact = count_paths(n, preds)
    assert exact == 2 ** e
    edges = instance(n, preds, [n - 1 - i for i in range(n)])
    t1 = time.time()
    got = p1786.countRestrictedPaths(n, edges)
    t1 = time.time() - t1
    print(f"  1786's program on it: n = {n}, m = {len(edges)}, answer {got}, "
          f"{'matches' if got == exact % MOD else 'DOES NOT MATCH'} 2^{e} mod p, {t1:.2f} s")
    for name, (n, preds) in (("K4 chain alone", chain_preds([4] * 6666)),
                             ("K5 chain alone", chain_preds([5] * 4000)),
                             ("K3 chain alone", chain_preds([3] * 9999)),
                             ("ladder, width 2", layered_preds(2, 9999)),
                             ("layers of three", layered_preds(3, 4444)),
                             ("fibonacci strip", (N, strip_preds(N, {}))),
                             ("K4 start strip", (N, strip_preds(N, {3: 3}))),
                             ("K4 start, 4 at end", (N, strip_preds(N, {3: 3, N - 1: 4})))):
        m = sum(bin(p).count("1") for p in preds)
        print(f"  {name:18s} n = {n:5d} m = {m:5d} {digits(count_paths(n, preds)):5d} digits")
    preds = strip_preds(N, {3: 3, N - 1: 4})
    exact = count_paths(N, preds)
    edges = instance(N, preds, [N - 1 - i for i in range(N)])
    t1 = time.time()
    got = p1786.countRestrictedPaths(N, edges)
    t1 = time.time() - t1
    print(f"  1786's program on the K4-start strip with four at the end: n = {N}, m = {len(edges)}, answer {got}, "
          f"{'matches' if got == exact % MOD else 'DOES NOT MATCH'} the exact count, {t1:.2f} s")

    # 5. (Oct 20) the most paths for m edges with the node count free
    print("\n5. most paths on at most m edges, nodes free: strips of any length against the exhaustive n <= 9")
    one, _ = strip_free(20, kmin=1)
    two, how = strip_free(44)
    print(f"  in-degree 1 allowed past node 1 changes the strip maximum at m <= 20 on "
          f"{sum(one[m] != two[m] for m in range(1, 21))} cells")
    ex9 = exhaustive(9)
    fits = [m for m in range(1, 37) if len(how[m]) + 1 <= 9]
    agree = sum(ex9[m] == two[m] for m in fits)
    print(f"  exhaustive at n <= 9 against the strip, where the strip fits in 9 nodes (m <= {fits[-1]}): "
          f"{agree} of {len(fits)} agree")
    for m in range(fits[-1] + 1, 23):
        print(f"    m = {m}: exhaustive n <= 9 {ex9[m]}, strip {two[m]} on {len(how[m]) + 1} nodes")
    shapes = {}
    for m in range(3, 45):
        tail = how[m][1:]
        key = "all 2" if set(tail) == {2} else ("2s, sink on 3" if set(tail[:-1]) <= {2} and tail[-1] == 3 else str(how[m]))
        shapes.setdefault(key, []).append(m)
    for key, ms in shapes.items():
        print(f"  {key:14s} at m = {ms[0]}..{ms[-1]}, {len(ms)} cells")
    for m in (21, 30, 37, 43, 44):
        print(f"  m = {m}: {two[m]}, against m - 2 {two[m] / two[m - 2]:.5f}, per edge {two[m] ** (1 / m):.4f}")
    print(f"  phi {(1 + 5 ** 0.5) / 2:.5f}, its square root {((1 + 5 ** 0.5) / 2) ** 0.5:.4f}")
    for n, m in ((13, 22), (17, 30), (20, 36)):
        print(f"  climber at n = {n}, m = {m}: {climb(rng, n, m, 3000, 20)} against the strip's {two[m]}")

    # 6. (Oct 22) the rewrite to the largest earlier counts: every DAG is beaten by a strip
    print("\n6. every node's predecessors moved to the earlier nodes with the largest counts")
    tried = lower = 0
    near = {}
    for _ in range(20000):
        n = rng.randrange(4, 21)
        pr = pairs(n)
        dens = rng.random()
        preds = preds_of(n, pr, sum(1 << b for b in range(len(pr)) if rng.random() < dens))
        m = sum(bin(p).count("1") for p in preds)
        old = count_paths(n, preds)
        widths, new = top_rewrite(n, preds)
        k = len(widths) + 1
        assert sum(widths) == m and k <= n
        assert count_paths(k, strip_preds(k, {j + 1: w for j, w in enumerate(widths)})) == new
        tried += 1
        lower += new < old
        if m <= 44:
            assert old <= two[m], (n, m, old)
            if 20 <= m <= 30 and old / two[m] > near.get(m, 0):
                near[m] = old / two[m]
    print(f"  {lower} of {tried} random DAGs on 4 to 20 nodes counted fewer paths after the rewrite, "
          f"which keeps the edges and never adds a node")
    print("  best random DAG against the strip at m = 20..30: "
          + " ".join(f"{m}:{near[m]:.2f}" for m in sorted(near)))
    t1 = time.time()
    beat, done = strip_any(32, two, 120)
    print(f"  strips with any in-degree, pruned by count x largest part product, m <= 32: "
          f"{'finished' if done else 'out of time'}, {len(beat)} cells beat in-degrees 2 to 5, "
          f"{time.time() - t1:.0f} s")

    print(f"\n{time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
