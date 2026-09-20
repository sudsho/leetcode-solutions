import heapq
import itertools
import math
import random
import time
from fractions import Fraction
from typing import List, Sequence, Tuple


def adjacency(n: int, edges: Sequence[Sequence[int]], prob: Sequence) -> List[List[Tuple[int, object]]]:
    """(neighbour, edge probability) per node, both directions."""
    adj: List[List[Tuple[int, object]]] = [[] for _ in range(n)]
    for (u, v), p in zip(edges, prob):
        adj[u].append((v, p))
        adj[v].append((u, p))
    return adj


def dijkstra_product(n: int, adj, src: int, one, flip: bool = False, guard: bool = False):
    """Best product from src to every node, settling the largest first.

    The settle argument is the one the last five problems have been about, and
    it does not mention addition anywhere. A node popped with product p is
    final because every other route to it still in the heap starts at some
    q <= p and can only be multiplied by factors in [0, 1] from here on. What
    carries the argument is that the update never improves a value, not that it
    is a sum. `flip` breaks heap ties on the larger id, the same knob 1786 and
    3123 used.

    `guard` refuses to write into a node that has already settled. With factors
    in [0, 1] no such write can ever land, so the flag does nothing and is not
    worth paying for; the p > 1 section is the only place it shows.
    """
    zero = type(one)(0)
    best = [zero] * n
    best[src] = one
    done = [False] * n
    heap = [(-one, -src if flip else src)]
    while heap:
        neg, key = heapq.heappop(heap)
        u = -key if flip else key
        if done[u]:
            continue
        done[u] = True
        p = -neg
        for v, q in adj[u]:
            if guard and done[v]:
                continue
            if p * q > best[v]:
                best[v] = p * q
                heapq.heappush(heap, (-(p * q), -v if flip else v))
    return best


def neg_log_costs(n: int, adj, src: int) -> List[float]:
    """The same walk over -log p, which turns the product into a sum. Returns the costs, not the products.

    A zero-probability edge is dropped rather than given an infinite cost: it
    can never be on a route whose product is positive, and if every route uses
    one the answer is 0 either way.
    """
    inf = float("inf")
    cost = [inf] * n
    cost[src] = 0.0
    done = [False] * n
    heap = [(0.0, src)]
    while heap:
        c, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, q in adj[u]:
            if q <= 0.0:
                continue
            nxt = c - math.log(q)
            if nxt < cost[v]:
                cost[v] = nxt
                heapq.heappush(heap, (nxt, v))
    return cost


def dijkstra_neg_log(n: int, adj, src: int) -> List[float]:
    """The costs read back as probabilities. The exponential is where the long chains lose everything."""
    return [0.0 if c == float("inf") else math.exp(-c) for c in neg_log_costs(n, adj, src)]


def oracle(n: int, edges, prob, start: int, end: int) -> Tuple[Fraction, int]:
    """Every simple path from start to end, enumerated: the largest exact product and how many paths attain it.

    No heap and no settle. With factors in [0, 1] a repeated node can only cost
    product, so the simple paths hold the best route; the p > 1 section below
    reads this as the best *simple* path instead, which is where the two part
    company. The count is there for the tie-break question, which needs to know
    how often there is anything to break.
    """
    adj = adjacency(n, edges, prob)
    best = Fraction(0)
    attaining = 0
    stack = [(start, Fraction(1), 1 << start)]
    while stack:
        u, p, seen = stack.pop()
        if u == end:
            if p > best:
                best, attaining = p, 0
            if p == best:
                attaining += 1
            continue
        for v, q in adj[u]:
            if not seen >> v & 1:
                stack.append((v, p * q, seen | 1 << v))
    return best, attaining


class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float],
                       start_node: int, end_node: int) -> float:
        """Dijkstra on the product, largest first.

        The alternatives, and the two places the argument stops holding, are in
        `__main__`.
        """
        adj = adjacency(n, edges, succProb)
        return dijkstra_product(n, adj, start_node, 1.0)[end_node]


def graphs(n: int, values: Tuple[Fraction, ...]):
    """Every simple graph on 0..n-1 with edge probabilities from `values`, connected or not."""
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product((None,) + values, repeat=len(pairs)):
        picked = [(pair, p) for pair, p in zip(pairs, choice) if p is not None]
        yield [list(pair) for pair, _ in picked], [p for _, p in picked]


def random_graph(rng: random.Random, n: int, m: int, values: Sequence[Fraction]):
    chosen = {}
    target = min(m, n * (n - 1) // 2)
    while len(chosen) < target:
        u, v = rng.sample(range(n), 2)
        chosen.setdefault((min(u, v), max(u, v)), rng.choice(values))
    return [[u, v] for u, v in chosen], list(chosen.values())


def chain(length: int, p: float):
    """A single path of `length` edges all of probability p."""
    return length + 1, [[i, i + 1] for i in range(length)], [p] * length


if __name__ == "__main__":
    rng = random.Random(1514)
    started = time.time()

    print("== exhaustive: every simple graph, 0 to n-1, exact arithmetic ==")
    half = (Fraction(1, 4), Fraction(1, 2), Fraction(1))
    for n, values in ((3, half), (4, half), (5, (Fraction(1, 2), Fraction(1)))):
        total = reachable = ties = 0
        wrong_exact = wrong_flip = 0
        for edges, prob in graphs(n, values):
            total += 1
            truth, attaining = oracle(n, edges, prob, 0, n - 1)
            adj = adjacency(n, edges, prob)
            got = dijkstra_product(n, adj, 0, Fraction(1))[n - 1]
            flipped = dijkstra_product(n, adj, 0, Fraction(1), flip=True)[n - 1]
            wrong_exact += got != truth
            wrong_flip += flipped != truth
            reachable += truth > 0
            # more than one route attains the best product: 3123's tied shortest paths, one problem on
            ties += truth > 0 and attaining > 1
        print(f"  n={n} values={tuple(str(v) for v in values)}  graphs {total}  reachable {reachable}"
              f"   tied best routes {ties}"
              f"   exact dijkstra wrong {wrong_exact}   flipped tie-break wrong {wrong_flip}")

    print("\n== float against exact, tenths, every simple graph at n = 4 ==")
    tenths = (Fraction(1, 10), Fraction(3, 10), Fraction(9, 10))
    total = differ_any = differ_1e9 = differ_1e6 = 0
    worst = 0.0
    for edges, prob in graphs(4, tenths):
        total += 1
        truth = oracle(4, edges, prob, 0, 3)[0]
        adj = adjacency(4, edges, [float(p) for p in prob])
        got = dijkstra_product(4, adj, 0, 1.0)[3]
        log_got = dijkstra_neg_log(4, adj, 0)[3]
        gap = abs(got - float(truth))
        worst = max(worst, gap, abs(log_got - float(truth)))
        differ_any += Fraction(got) != truth
        differ_1e9 += gap > 1e-9
        differ_1e6 += gap > 1e-6
        assert abs(log_got - float(truth)) < 1e-9
    print(f"  graphs {total}   float not exactly equal {differ_any}   off by >1e-9 {differ_1e9}"
          f"   off by >1e-6 {differ_1e6}   worst gap {worst:.3e}")

    print("\n== random graphs, n = 10, float and neg-log against exact ==")
    for m, values in ((12, tenths), (25, tenths), (25, (Fraction(99, 100),)), (25, (Fraction(0), Fraction(1, 2), Fraction(1)))):
        worst_p = worst_l = 0.0
        disagree = 0
        for _ in range(1000):
            edges, prob = random_graph(rng, 10, m, values)
            truth = float(oracle(10, edges, prob, 0, 9)[0])
            adj = adjacency(10, edges, [float(p) for p in prob])
            p_got = dijkstra_product(10, adj, 0, 1.0)[9]
            l_got = dijkstra_neg_log(10, adj, 0)[9]
            worst_p = max(worst_p, abs(p_got - truth))
            worst_l = max(worst_l, abs(l_got - truth))
            disagree += p_got != l_got
        names = tuple(str(v) for v in values)
        print(f"  m={m:3d} values={names}  product worst {worst_p:.3e}   neg-log worst {worst_l:.3e}"
              f"   the two disagree {disagree}/1000")

    print("\n== probabilities above 1, outside the statement, against the best simple path ==")
    over = (Fraction(1, 2), Fraction(3, 2))
    for n in (4, 5):
        total = 0
        tally = {False: [0, 0, 0], True: [0, 0, 0]}  # guard -> [wrong, too big, too small]
        for edges, prob in graphs(n, over):
            total += 1
            truth = oracle(n, edges, prob, 0, n - 1)[0]
            adj = adjacency(n, edges, prob)
            for g in (False, True):
                got = dijkstra_product(n, adj, 0, Fraction(1), guard=g)[n - 1]
                if got != truth:
                    tally[g][0] += 1
                    tally[g][1] += got > truth
                    tally[g][2] += got < truth
        for g in (False, True):
            w, big, small = tally[g]
            label = "with the done check" if g else "as written"
            print(f"  n={n} {label:20s} graphs {total}   wrong {w:6d}   too big {big:6d}   too small {small:6d}")

    print("\n== a chain of equal factors: where each form gives up ==")
    s = Solution()
    limit = 20000
    for p in (0.5, 0.9, 0.99):
        lo, hi = 1, limit
        while lo < hi:
            mid = (lo + hi) // 2
            n, edges, prob = chain(mid, p)
            if s.maxProbability(n, edges, prob, 0, n - 1) == 0.0:
                hi = mid
            else:
                lo = mid + 1
        n, edges, prob = chain(lo, p)
        got = s.maxProbability(n, edges, prob, 0, n - 1)
        true_log10 = lo * math.log10(p)
        if got == 0.0:
            where = f"reaches 0 at {lo} edges"
        elif got < 2.3e-308:
            where = f"never reaches 0 below {limit}, pinned in the subnormals at {got:.3e}"
        else:
            where = f"still an ordinary float at {limit} edges, {got:.3e}"
        print(f"  p={p:<5} {where};  the true value at {lo} edges is 1e{true_log10:.0f}")

    for length in (2000, 10000):
        n, edges, prob = chain(length, 0.9)
        worse = [0.8] * length
        a = s.maxProbability(n, edges, prob, 0, n - 1)
        b = s.maxProbability(n, edges, worse, 0, n - 1)
        ca = neg_log_costs(n, adjacency(n, edges, prob), 0)[n - 1]
        cb = neg_log_costs(n, adjacency(n, edges, worse), 0)[n - 1]
        print(f"  {length} edges: product gives {a:.3e} for 0.9 and {b:.3e} for 0.8"
              f" (true 1e{length * math.log10(0.9):.0f} and 1e{length * math.log10(0.8):.0f});"
              f"  neg-log costs {ca:.1f} and {cb:.1f}, exact to {abs(ca + length * math.log(0.9)):.1e}")

    print("\n== the statement's size, timed ==")
    for n, m in ((10000, 20000), (10000, 10000)):
        edges, prob = random_graph(rng, n, m, [Fraction(rng.randint(1, 100), 100) for _ in range(50)])
        prob = [float(p) for p in prob]
        t0 = time.time()
        answer = s.maxProbability(n, edges, prob, 0, n - 1)
        took = time.time() - t0
        log_answer = dijkstra_neg_log(n, adjacency(n, edges, prob), 0)[n - 1]
        print(f"  n={n} m={len(edges)}  answer {answer:.6g}   neg-log {log_answer:.6g}"
              f"   gap {abs(answer - log_answer):.3e}   {took:.2f}s")

    print(f"\n{time.time() - started:.0f}s")
