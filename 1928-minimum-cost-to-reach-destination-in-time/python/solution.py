import heapq
import itertools
import random
import time
from typing import List

INF = float("inf")


def adjacency(n, edges):
    adj = [[] for _ in range(n)]
    for e in edges:
        x, y, t = e[:3]
        toll = e[3] if len(e) > 3 else 0
        adj[x].append((y, t, toll))
        adj[y].append((x, t, toll))
    return adj


def pareto(max_time, edges, fees, bar_at_push=False):
    """Dijkstra on cost, keeping one number per city: the least time any popped state reached it in.

    Pops come out in cost order, so every earlier pop at a city was no dearer,
    and a new pop is dominated exactly when it is also no faster. The time bar
    is then the whole Pareto frontier the search needs, and a state is expanded
    only if it beats it. `bar_at_push=True` moves the bar update to the push,
    where the state setting it has not been shown to be the cheapest yet. That
    is still right here, because what a push into v costs is the popped cost
    plus fees[v], and popped costs only grow. Put a toll on the edge, a fourth
    entry in `edges` that no statement case has, and the argument is gone.
    """
    n = len(fees)
    adj = adjacency(n, edges)
    bar = [INF] * n
    heap = [(fees[0], 0, 0)]
    if bar_at_push:
        bar[0] = 0
    while heap:
        cost, t, u = heapq.heappop(heap)
        if u == n - 1:
            return cost
        if not bar_at_push:
            if t >= bar[u]:
                continue
            bar[u] = t
        for v, w, toll in adj[u]:
            nt = t + w
            if nt <= max_time and nt < bar[v]:
                if bar_at_push:
                    bar[v] = nt
                heapq.heappush(heap, (cost + fees[v] + toll, nt, v))
    return -1


def settle_once(max_time, edges, fees, key="cost"):
    """Plain Dijkstra that settles each city the first time it pops, ordered by cost or by time.

    Either order keeps one label per city, which is the state the problem
    does not have: the cheapest arrival may be too slow to finish, and the
    fastest may be the expensive one.
    """
    n = len(fees)
    adj = adjacency(n, edges)
    done = [False] * n
    heap = [(fees[0], 0, 0) if key == "cost" else (0, fees[0], 0)]
    while heap:
        a, b, u = heapq.heappop(heap)
        cost, t = (a, b) if key == "cost" else (b, a)
        if done[u]:
            continue
        done[u] = True
        if u == n - 1:
            return cost
        for v, w, toll in adj[u]:
            if not done[v] and t + w <= max_time:
                nc, nt = cost + fees[v] + toll, t + w
                heapq.heappush(heap, (nc, nt, v) if key == "cost" else (nt, nc, v))
    return -1


def oracle(max_time, edges, fees):
    """at[t][v] is the least cost of a walk that is at v at exactly time t. Nothing is settled.

    Every edge takes at least one minute, so the table is filled in increasing
    t and each entry only reads smaller ones. Walks may revisit a city and pay
    for it again, which the statement allows and which never helps.
    """
    n = len(fees)
    adj = adjacency(n, edges)
    at = [[INF] * n for _ in range(max_time + 1)]
    at[0][0] = fees[0]
    for t in range(max_time + 1):
        for u in range(n):
            if at[t][u] < INF:
                for v, w, toll in adj[u]:
                    if t + w <= max_time and at[t][u] + fees[v] + toll < at[t + w][v]:
                        at[t + w][v] = at[t][u] + fees[v] + toll
    best = min(at[t][n - 1] for t in range(max_time + 1))
    return -1 if best == INF else best


def frontier_sizes(max_time, edges, fees):
    """How many states per city the Pareto search expands, run to exhaustion."""
    n = len(fees)
    adj = adjacency(n, edges)
    bar = [INF] * n
    count = [0] * n
    heap = [(fees[0], 0, 0)]
    while heap:
        cost, t, u = heapq.heappop(heap)
        if t >= bar[u]:
            continue
        bar[u] = t
        count[u] += 1
        for v, w, toll in adj[u]:
            if t + w <= max_time and t + w < bar[v]:
                heapq.heappush(heap, (cost + fees[v] + toll, t + w, v))
    return count


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        """Dijkstra on cost with a time bar per city. The rest is in `__main__`."""
        return pareto(maxTime, edges, passingFees)


def random_graph(rng, n, m, top_t, top_f, top_toll=0):
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, top_t), rng.randint(0, top_toll)) for _ in range(m)]
    edges = [e for e in edges if e[0] != e[1]]
    return edges, [rng.randint(1, top_f) for _ in range(n)]


if __name__ == "__main__":
    rng = random.Random(1928)
    started = time.time()
    solvers = {
        "pareto": lambda T, e, f: pareto(T, e, f),
        "bar at push": lambda T, e, f: pareto(T, e, f, bar_at_push=True),
        "settle by cost": lambda T, e, f: settle_once(T, e, f, "cost"),
        "settle by time": lambda T, e, f: settle_once(T, e, f, "time"),
    }

    print("== every graph on 4 cities, edge times in {absent, 1, 2}, fees in 1..3, maxTime 1..6 ==")
    pairs = list(itertools.combinations(range(4), 2))
    wrong = dict.fromkeys(solvers, 0)
    total = reachable = 0
    for times in itertools.product((0, 1, 2), repeat=len(pairs)):
        edges = [(x, y, t) for (x, y), t in zip(pairs, times) if t]
        for fees in itertools.product((1, 2, 3), repeat=4):
            for T in range(1, 7):
                want = oracle(T, edges, fees)
                total += 1
                reachable += want != -1
                for name, f in solvers.items():
                    wrong[name] += f(T, edges, fees) != want
    print(f"  instances {total}   answer exists {reachable}")
    for name, k in wrong.items():
        print(f"  {name:15s} wrong {k:6d}   {100 * k / reachable:.2f}% of the answerable")

    print("\n== every graph on 5 cities, edge times in {absent, 1, 3}, end fees 1, middle fees 1..2, maxTime 2..8 ==")
    pairs = list(itertools.combinations(range(5), 2))
    wrong = dict.fromkeys(solvers, 0)
    total = reachable = 0
    for times in itertools.product((0, 1, 3), repeat=len(pairs)):
        edges = [(x, y, t) for (x, y), t in zip(pairs, times) if t]
        for mid in itertools.product((1, 2), repeat=3):
            fees = (1,) + mid + (1,)
            for T in range(2, 9):
                want = oracle(T, edges, fees)
                total += 1
                reachable += want != -1
                for name, f in solvers.items():
                    wrong[name] += f(T, edges, fees) != want
    print(f"  instances {total}   answer exists {reachable}")
    for name, k in wrong.items():
        print(f"  {name:15s} wrong {k:6d}   {100 * k / reachable:.2f}% of the answerable")

    print("\n== random multigraphs ==")
    for n, m, top_t, top_f, toll, T, count in ((6, 10, 5, 10, 0, 12, 4000), (10, 20, 10, 100, 0, 30, 2000),
                                               (30, 60, 20, 1000, 0, 100, 300), (6, 10, 5, 10, 10, 12, 4000),
                                               (10, 20, 10, 100, 100, 30, 2000)):
        wrong = dict.fromkeys(solvers, 0)
        live = 0
        for _ in range(count):
            edges, fees = random_graph(rng, n, m, top_t, top_f, toll)
            want = oracle(T, edges, fees)
            live += want != -1
            for name, f in solvers.items():
                wrong[name] += f(T, edges, fees) != want
        print(f"  n {n:2d} m {m:2d} tolls 0..{toll:<3d} maxTime {T:3d}  graphs {count}  answerable {live}   "
              + "   ".join(f"{k} {v}" for k, v in wrong.items()))

    print("\n== the statement's size: edges <= 1000, maxTime = 1000, fees to 1000 ==")
    s = Solution()
    for n, top_t in ((1000, 10), (100, 50), (100, 200), (30, 100)):
        # a random tree so city n - 1 is reachable, then random edges up to 1000
        edges = [(i, rng.randrange(i), rng.randint(1, top_t)) for i in range(1, n)]
        extra, fees = random_graph(rng, n, 1000 - len(edges), top_t, 1000)
        edges += [e[:3] for e in extra]
        t0 = time.time()
        ans = s.minCost(1000, edges, fees)
        el = time.time() - t0
        sizes = frontier_sizes(1000, edges, fees)
        hit = [c for c in sizes if c]
        print(f"  n {n:4d} edges {len(edges):4d} times 1..{top_t:<4d} answer {ans:6d} in {el:.3f}s"
              f"   oracle {oracle(1000, edges, fees):6d}   states per city mean {sum(hit) / len(hit):.2f} max {max(sizes)}")

    print(f"\n{time.time() - started:.0f}s")
