import heapq
import itertools
import random
import time
from typing import List

INF = float("inf")


def adjacency(n, highways):
    adj = [[] for _ in range(n)]
    for a, b, toll in highways:
        adj[a].append((b, toll))
        adj[b].append((a, toll))
    return adj


def layered(n, highways, discounts):
    """Dijkstra on (city, discounts used), each of the k + 1 layers of a city settled once."""
    adj = adjacency(n, highways)
    done = [[False] * (discounts + 1) for _ in range(n)]
    heap = [(0, 0, 0)]
    while heap:
        cost, u, used = heapq.heappop(heap)
        if done[u][used]:
            continue
        done[u][used] = True
        if u == n - 1:
            return cost
        for v, toll in adj[u]:
            if not done[v][used]:
                heapq.heappush(heap, (cost + toll, v, used))
            if used < discounts and not done[v][used + 1]:
                heapq.heappush(heap, (cost + toll // 2, v, used + 1))
    return -1


def pareto(n, highways, discounts, bar_at_push=False):
    """Dijkstra on cost keeping one number per city: the most discounts any popped state still had there.

    The same argument as 1928's time bar. Pops come in cost order, so a pop is
    dominated exactly when it has no more discounts left than an earlier pop at
    the same city, and a discount left over never hurts. `bar_at_push=True`
    sets the bar when the state is pushed. In 1928 that was right because the
    fee sat on the city; here the toll is on the road and a discounted push
    and a full-price push into the same city come in no particular cost order.
    """
    adj = adjacency(n, highways)
    bar = [-1] * n
    heap = [(0, -discounts, 0)]
    if bar_at_push:
        bar[0] = discounts
    while heap:
        cost, neg_left, u = heapq.heappop(heap)
        left = -neg_left
        if u == n - 1:
            return cost
        if not bar_at_push:
            if left <= bar[u]:
                continue
            bar[u] = left
        for v, toll in adj[u]:
            for nc, nl in ((cost + toll, left), (cost + toll // 2, left - 1)):
                if nl >= 0 and nl > bar[v]:
                    if bar_at_push:
                        bar[v] = nl
                    heapq.heappush(heap, (nc, -nl, v))
    return -1


def one_label(n, highways, discounts):
    """Plain Dijkstra with one label per city, the cheapest arrival, carrying whatever discounts it had left.

    Every road out of a settled city is offered both ways while a discount
    remains, so this is the layered search with the layers merged. The cheap
    arrival may have spent the discount the rest of the route wanted.
    """
    adj = adjacency(n, highways)
    done = [False] * n
    heap = [(0, -discounts, 0)]
    while heap:
        cost, neg_left, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        if u == n - 1:
            return cost
        for v, toll in adj[u]:
            if not done[v]:
                heapq.heappush(heap, (cost + toll, neg_left, v))
                if neg_left < 0:
                    heapq.heappush(heap, (cost + toll // 2, neg_left + 1, v))
    return -1


def discount_after(n, highways, discounts):
    """The shortest route at full price, then the discounts spent on its k dearest roads."""
    adj = adjacency(n, highways)
    dist = [INF] * n
    prev = [None] * n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, toll in adj[u]:
            if d + toll < dist[v]:
                dist[v], prev[v] = d + toll, (u, toll)
                heapq.heappush(heap, (d + toll, v))
    if dist[n - 1] == INF:
        return -1
    tolls, v = [], n - 1
    while v != 0:
        u, toll = prev[v]
        tolls.append(toll)
        v = u
    return route_cost(tolls, discounts)


def route_cost(tolls, discounts):
    """A fixed route's cost with the discounts on its dearest roads, which is where they save most."""
    tolls = sorted(tolls, reverse=True)
    return sum(t // 2 for t in tolls[:discounts]) + sum(tolls[discounts:])


def oracle_costs(n, highways, top_k):
    """The least cost for every k in 0..top_k over all simple paths, each discounted on its dearest roads.

    Nothing is settled and no state is kept. Walks need not be counted: cutting
    a cycle out of a walk never raises its toll and frees whatever discounts it
    used, so the statement's once-per-highway rule is never what binds.
    """
    adj = adjacency(n, highways)
    best = [INF] * (top_k + 1)
    seen = [False] * n
    tolls = []

    def walk(u):
        if u == n - 1:
            for k in range(top_k + 1):
                c = route_cost(tolls, k)
                if c < best[k]:
                    best[k] = c
            return
        seen[u] = True
        for v, toll in adj[u]:
            if not seen[v]:
                tolls.append(toll)
                walk(v)
                tolls.pop()
        seen[u] = False

    walk(0)
    return [-1 if b == INF else b for b in best]


def pareto_states(n, highways, discounts):
    """How many states per city the Pareto search expands, run to exhaustion."""
    adj = adjacency(n, highways)
    bar = [-1] * n
    count = [0] * n
    heap = [(0, -discounts, 0)]
    while heap:
        cost, neg_left, u = heapq.heappop(heap)
        if -neg_left <= bar[u]:
            continue
        bar[u] = -neg_left
        count[u] += 1
        for v, toll in adj[u]:
            for nc, nl in ((cost + toll, -neg_left), (cost + toll // 2, -neg_left - 1)):
                if nl >= 0 and nl > bar[v]:
                    heapq.heappush(heap, (nc, -nl, v))
    return count


class Solution:
    def minimumCost(self, n: int, highways: List[List[int]], discounts: int) -> int:
        """Dijkstra on cost with a discounts-left bar per city. The rest is in `__main__`."""
        return pareto(n, highways, discounts)


def random_graph(rng, n, m, top_toll):
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, top_toll)) for _ in range(m)]
    return [e for e in edges if e[0] != e[1]]


if __name__ == "__main__":
    rng = random.Random(2093)
    started = time.time()
    solvers = {
        "layered": layered,
        "pareto": pareto,
        "bar at push": lambda n, h, k: pareto(n, h, k, bar_at_push=True),
        "one label": one_label,
        "discount after": discount_after,
    }

    def exhaust(n, values, top_k):
        pairs = list(itertools.combinations(range(n), 2))
        wrong = dict.fromkeys(solvers, 0)
        total = reachable = 0
        for tolls in itertools.product(values, repeat=len(pairs)):
            h = [(a, b, t) for (a, b), t in zip(pairs, tolls) if t is not None]
            want = oracle_costs(n, h, top_k)
            for k in range(top_k + 1):
                total += 1
                reachable += want[k] != -1
                for name, f in solvers.items():
                    wrong[name] += f(n, h, k) != want[k]
        return total, reachable, wrong

    for n, values, top_k in ((4, (None, 1, 3, 4), 3), (5, (None, 1, 4), 2), (5, (None, 2, 7), 2),
                             (5, (None, 0, 3), 2)):
        total, reachable, wrong = exhaust(n, values, top_k)
        print(f"== every graph on {n} cities, tolls in {values}, discounts 0..{top_k} ==")
        print(f"  instances {total}   answer exists {reachable}")
        for name, k in wrong.items():
            print(f"  {name:15s} wrong {k:6d}   {100 * k / reachable:.2f}% of the answerable")

    print("\n== random multigraphs, tolls from 0 ==")
    for n, m, top_toll, k, count in ((6, 10, 10, 1, 4000), (6, 10, 10, 2, 4000), (8, 16, 100, 2, 2000),
                                     (10, 20, 100, 3, 1000), (10, 30, 1000, 5, 500)):
        wrong = dict.fromkeys(solvers, 0)
        live = 0
        for _ in range(count):
            h = random_graph(rng, n, m, top_toll)
            want = oracle_costs(n, h, k)[k]
            live += want != -1
            for name, f in solvers.items():
                wrong[name] += f(n, h, k) != want
        print(f"  n {n:2d} m {m:2d} tolls 0..{top_toll:<5d} k {k}  graphs {count}  answerable {live}   "
              + "   ".join(f"{a} {b}" for a, b in wrong.items()))

    print("\n== the statement's size: n <= 1000, highways <= 1000, tolls to 1e5, discounts <= 500 ==")
    s = Solution()
    for n, extra, k in ((1000, 1, 500), (1000, 1, 5), (200, 800, 5), (200, 800, 500), (50, 950, 20)):
        h = [(i, rng.randrange(i), rng.randint(0, 10 ** 5)) for i in range(1, n)]
        h += random_graph(rng, n, extra, 10 ** 5)
        h = h[:1000]
        t0 = time.time()
        ans = s.minimumCost(n, h, k)
        el_p = time.time() - t0
        t0 = time.time()
        ref = layered(n, h, k)
        el_l = time.time() - t0
        sizes = pareto_states(n, h, k)
        hit = [c for c in sizes if c]
        print(f"  n {n:4d} highways {len(h):4d} k {k:3d}  pareto {ans} in {el_p:.3f}s   layered {ref} in {el_l:.3f}s"
              f"   states per city mean {sum(hit) / len(hit):.2f} max {max(sizes)} of {k + 1}")

    print(f"\n{time.time() - started:.0f}s")
