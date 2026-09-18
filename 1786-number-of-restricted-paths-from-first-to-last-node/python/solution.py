import heapq
import itertools
import random
import time
from typing import Dict, List, Tuple

MOD = 10 ** 9 + 7


def adjacency(n: int, edges: List[List[int]]) -> List[List[Tuple[int, int]]]:
    adj: List[List[Tuple[int, int]]] = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def distances(n: int, adj, flip: bool = False) -> Tuple[List[int], List[int]]:
    """Dijkstra from node n. Returns the distances and the order nodes were settled in.

    `flip` breaks heap ties on the larger node id instead of the smaller, which
    changes nothing about the distances and is only there so the order among
    equal distances can be moved around from outside.
    """
    inf = float("inf")
    dist = [inf] * (n + 1)
    dist[n] = 0
    heap = [(0, -n if flip else n)]
    order = []
    done = [False] * (n + 1)
    while heap:
        d, key = heapq.heappop(heap)
        u = -key if flip else key
        if done[u]:
            continue
        done[u] = True
        order.append(u)
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, -v if flip else v))
    return dist, order


def pull(n: int, adj, dist, order, keep, mod=None) -> List[int]:
    """Count restricted paths into every node at the moment it is settled.

    A restricted path from u to n steps to a neighbour strictly closer to n each
    time, so ways(u) is the sum of ways(v) over neighbours with dist[v] < dist[u],
    and all of those are settled before u because they are strictly closer.
    `keep(du, dv)` is the filter on which settled neighbours count, and the three
    candidates are compared in `__main__`.
    """
    ways = [0] * (n + 1)
    settled = [False] * (n + 1)
    for u in order:
        if u == n:
            ways[u] = 1
        else:
            total = 0
            for v, _ in adj[u]:
                if settled[v] and keep(dist[u], dist[v]):
                    total += ways[v]
            ways[u] = total % mod if mod else total
        settled[u] = True
    return ways


def strict(du, dv):
    return dv < du


def weak(du, dv):
    return dv <= du


def unfiltered(du, dv):
    return True


def oracle(n: int, edges: List[List[int]]) -> int:
    """Every simple path from 1 to n, enumerated, and kept if the distances along it strictly fall.

    It never uses the recursion. A strictly falling path cannot repeat a node, so
    the simple paths are all of them, and the distances come from Floyd-Warshall
    rather than from the Dijkstra the solution uses.
    """
    inf = float("inf")
    d = [[inf] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
        d[v][u] = min(d[v][u], w)
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    nbrs = {u: set() for u in range(1, n + 1)}
    for u, v, _ in edges:
        nbrs[u].add(v)
        nbrs[v].add(u)
    count = 0
    stack = [(1, 1 << 1)]
    while stack:
        u, seen = stack.pop()
        if u == n:
            count += 1
            continue
        for v in nbrs[u]:
            if not seen >> v & 1 and d[v][n] < d[u][n]:
                stack.append((v, seen | 1 << v))
    return count


class Solution:
    def countRestrictedPaths(self, n: int, edges: List[List[int]]) -> int:
        """Dijkstra from n, then the count pulled at each settle with a strict filter.

        Which filter the pull needs, and what an equal distance between two
        neighbours does to the ones that are wrong, is run in `__main__`.
        """
        adj = adjacency(n, edges)
        dist, order = distances(n, adj)
        return pull(n, adj, dist, order, strict, MOD)[1]


def graphs(n: int, weights: Tuple[int, ...]):
    """Every connected simple graph on 1..n with edge weights from `weights`."""
    pairs = list(itertools.combinations(range(1, n + 1), 2))
    for choice in itertools.product((0,) + weights, repeat=len(pairs)):
        edges = [[u, v, w] for (u, v), w in zip(pairs, choice) if w]
        parent = list(range(n + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for u, v, _ in edges:
            parent[find(u)] = find(v)
        if len({find(x) for x in range(1, n + 1)}) == 1:
            yield edges


def random_graph(rng: random.Random, n: int, extra: int, top: int) -> List[List[int]]:
    """A random spanning tree plus `extra` more edges, weights in 1..top, no repeated pairs."""
    edges = {}
    nodes = list(range(1, n + 1))
    rng.shuffle(nodes)
    for i in range(1, n):
        u, v = nodes[i], nodes[rng.randrange(i)]
        edges[(min(u, v), max(u, v))] = rng.randint(1, top)
    target = min(len(edges) + extra, n * (n - 1) // 2)
    while len(edges) < target:
        u, v = rng.sample(range(1, n + 1), 2)
        edges.setdefault((min(u, v), max(u, v)), rng.randint(1, top))
    return [[u, v, w] for (u, v), w in edges.items()]


def tied_edge(edges, dist, avoid=None) -> bool:
    """Whether some edge joins two nodes at the same distance from n, skipping edges that touch `avoid`."""
    return any(dist[u] == dist[v] and avoid not in (u, v) for u, v, _ in edges)


def run(n, edges) -> Dict[str, object]:
    adj = adjacency(n, edges)
    dist, order = distances(n, adj)
    _, flipped = distances(n, adj, flip=True)
    return {
        "strict": pull(n, adj, dist, order, strict)[1],
        "weak": pull(n, adj, dist, order, weak)[1],
        "none": pull(n, adj, dist, order, unfiltered)[1],
        "none flipped": pull(n, adj, dist, flipped, unfiltered)[1],
        "tied": tied_edge(edges, dist),
        # ties that do not touch node 1, which is where the ascending tie-break cannot protect the count
        "tied below 1": tied_edge(edges, dist, avoid=1),
    }


def ratio(a: int, b: int) -> str:
    try:
        return f"{a / b:.4g}"
    except OverflowError:
        return f"~1e{len(str(a)) - len(str(b))}"


def ladder(layers: int, rungs: bool) -> Tuple[int, List[List[int]]]:
    """Pairs of nodes, each joined to the next pair by all four unit edges, the last pair to n.

    Both nodes of a pair are the same distance from n, so with `rungs` every
    pair is also joined to itself by a tied edge. The count doubles per pair,
    2^(layers - 1) restricted paths from node 1, with or without the rungs,
    because a rung never falls.
    """
    n = 2 * layers + 1
    edges = []
    for k in range(layers - 1):
        a, b, c, d = 2 * k + 1, 2 * k + 2, 2 * k + 3, 2 * k + 4
        edges += [[a, c, 1], [a, d, 1], [b, c, 1], [b, d, 1]]
    edges += [[n - 2, n, 1], [n - 1, n, 1]]
    if rungs:
        edges += [[2 * k + 1, 2 * k + 2, 1] for k in range(layers)]
    return n, edges


if __name__ == "__main__":
    rng = random.Random(1786)
    started = time.time()

    print("== exhaustive: every connected graph ==")
    print("  n  weights    graphs   tied   strict wrong   weak wrong   none wrong   none flipped wrong"
          "   none: flip changes it   wrong outside tied")
    for n, weights in ((3, (1, 2, 3)), (4, (1, 2, 3)), (5, (1, 2))):
        total = tied = 0
        wrong = {"strict": 0, "weak": 0, "none": 0, "none flipped": 0}
        flip_changes = outside = 0
        default_wrong_above_only = 0
        for edges in graphs(n, weights):
            total += 1
            got = run(n, edges)
            truth = oracle(n, edges)
            tied += got["tied"]
            for key in wrong:
                if got[key] != truth:
                    wrong[key] += 1
                    if not got["tied"]:
                        outside += 1
            flip_changes += got["none"] != got["none flipped"]
            # settled already means dv <= du, so dropping the strict filter to <= changes nothing.
            assert got["weak"] == got["none"]
            if got["none"] != truth and not got["tied below 1"]:
                default_wrong_above_only += 1
        assert wrong["strict"] == 0 and outside == 0 and default_wrong_above_only == 0
        print(f"  {n}  {str(weights):9s} {total:7d}  {tied:5d}   {wrong['strict']:12d}   {wrong['weak']:10d}"
              f"   {wrong['none']:10d}   {wrong['none flipped']:18d}   {flip_changes:21d}   {outside:18d}")

    print("\n== random graphs, n = 9, spanning tree + extra edges ==")
    print("  extra  top   graphs   tied   weak wrong   none wrong   weak over   none over   mean ways")
    for extra, top in ((3, 1), (3, 3), (3, 10), (12, 1), (12, 3), (12, 10), (27, 10)):
        stats = {"tied": 0, "weak": 0, "none": 0, "weak over": 0, "none over": 0}
        ways_sum = 0
        for _ in range(2000):
            edges = random_graph(rng, 9, extra, top)
            got = run(9, edges)
            truth = oracle(9, edges)
            assert got["strict"] == truth
            ways_sum += truth
            stats["tied"] += got["tied"]
            for key in ("weak", "none"):
                if got[key] != truth:
                    stats[key] += 1
                    stats[key + " over"] += got[key] > truth
        print(f"  {extra:5d}  {top:3d}   {2000:6d}  {stats['tied']:5d}   {stats['weak']:10d}   {stats['none']:10d}"
              f"   {stats['weak over']:9d}   {stats['none over']:9d}   {ways_sum / 2000:9.2f}")

    print("\n== ladders at the statement's size, where the modulus is needed ==")
    s = Solution()
    for layers, rungs in ((20, False), (20, True), (7999, False), (7999, True)):
        n, edges = ladder(layers, rungs)
        adj = adjacency(n, edges)
        dist, order = distances(n, adj)
        exact = pull(n, adj, dist, order, strict)[1]
        loose = pull(n, adj, dist, order, unfiltered)[1]
        _, flipped = distances(n, adj, flip=True)
        loose_flip = pull(n, adj, dist, flipped, unfiltered)[1]
        assert exact == 2 ** (layers - 1)
        if layers == 20:
            assert exact == oracle(n, edges)
        t0 = time.time()
        answer = s.countRestrictedPaths(n, edges)
        took = time.time() - t0
        assert answer == exact % MOD
        print(f"  layers={layers:5d} rungs={str(rungs):5s} n={n:6d} m={len(edges):6d}  answer {answer:10d}"
              f"   exact {len(str(exact))} digits   unfiltered/exact {ratio(loose, exact)}"
              f"   flipped {ratio(loose_flip, exact)}   {took:.2f}s")

    print("\n== the statement's constraints, random, timed ==")
    for n, extra, top in ((20000, 20000, 100000), (20000, 20000, 1), (20000, 0, 1)):
        edges = random_graph(rng, n, extra, top)
        t0 = time.time()
        answer = s.countRestrictedPaths(n, edges)
        adj = adjacency(n, edges)
        dist, order = distances(n, adj)
        exact = pull(n, adj, dist, order, strict)[1]
        assert exact % MOD == answer
        print(f"  n={n}  m={len(edges)}  top={top}  answer {answer}   exact count {len(str(exact))} digits"
              f"   tied edges {sum(dist[u] == dist[v] for u, v, _ in edges)}   {time.time() - t0:.2f}s")

    print(f"\n{time.time() - started:.0f}s")
