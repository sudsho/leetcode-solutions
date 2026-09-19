import heapq
import itertools
import random
import time
from typing import Dict, List, Tuple


def adjacency(n: int, edges: List[List[int]]) -> List[List[Tuple[int, int, int]]]:
    """(neighbour, weight, edge index) per node, both directions."""
    adj: List[List[Tuple[int, int, int]]] = [[] for _ in range(n)]
    for i, (u, v, w) in enumerate(edges):
        adj[u].append((v, w, i))
        adj[v].append((u, w, i))
    return adj


def dijkstra(n: int, adj, src: int, flip: bool = False):
    """Distances from src, the settle order, and the edge each node was last relaxed through.

    `parent[v]` is the edge that set dist[v] to its final value first, which is
    whatever the heap handed over first among tied predecessors. `flip` breaks
    heap ties on the larger id, the same knob 1786 used, so the parent can be
    moved around from outside without changing any distance.
    """
    inf = float("inf")
    dist = [inf] * n
    parent = [-1] * n
    dist[src] = 0
    heap = [(0, -src if flip else src)]
    done = [False] * n
    order = []
    while heap:
        d, key = heapq.heappop(heap)
        u = -key if flip else key
        if done[u]:
            continue
        done[u] = True
        order.append(u)
        for v, w, i in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = i
                heapq.heappush(heap, (d + w, -v if flip else v))
    return dist, order, parent


def two_sided(n: int, edges, adj) -> List[bool]:
    """An edge is on a shortest 0 -> n-1 path iff going through it costs exactly the shortest distance."""
    d0 = dijkstra(n, adj, 0)[0]
    dn = dijkstra(n, adj, n - 1)[0]
    total = d0[n - 1]
    if total == float("inf"):
        return [False] * len(edges)
    return [d0[u] + w + dn[v] == total or d0[v] + w + dn[u] == total for u, v, w in edges]


def walk_back(n: int, edges, adj, keep) -> List[bool]:
    """One Dijkstra from 0, then walk back from n-1 over edges `keep(d0[u], w, d0[v])` names as predecessors.

    With `keep` the tight relation `d0[u] + w == d0[v]`, the edges reached are
    exactly the ones on some shortest path, since a tight edge into a node that
    is on a shortest path to n-1 extends one. The walk starts from n-1 and only
    ever moves to predecessors, so a tight edge off to the side is never seen.
    """
    d0 = dijkstra(n, adj, 0)[0]
    out = [False] * len(edges)
    if d0[n - 1] == float("inf"):
        return out
    seen = [False] * n
    seen[n - 1] = True
    stack = [n - 1]
    while stack:
        v = stack.pop()
        for u, w, i in adj[v]:
            if keep(d0[u], w, d0[v]):
                out[i] = True
                if not seen[u]:
                    seen[u] = True
                    stack.append(u)
    return out


def tight(du, w, dv):
    return du + w == dv


def closer(du, w, dv):
    """1786's filter: any neighbour strictly closer to the source."""
    return du < dv


def every_tight_edge(n: int, edges, adj) -> List[bool]:
    """Mark every edge with d0[u] + w == d0[v], without asking whether v leads on to n-1."""
    d0 = dijkstra(n, adj, 0)[0]
    if d0[n - 1] == float("inf"):
        return [False] * len(edges)
    return [d0[u] + w == d0[v] or d0[v] + w == d0[u] for u, v, w in edges]


def parent_chain(n: int, edges, adj, flip: bool = False) -> List[bool]:
    """The one shortest path the heap recorded, read back through the parent pointers."""
    dist, _, parent = dijkstra(n, adj, 0, flip)
    out = [False] * len(edges)
    if dist[n - 1] == float("inf"):
        return out
    v = n - 1
    while v != 0:
        i = parent[v]
        out[i] = True
        a, b, _ = edges[i]
        v = a if b == v else b
    return out


def oracle(n: int, edges) -> List[bool]:
    """Every simple path from 0 to n-1, enumerated, and the edges of the cheapest ones marked.

    With positive weights a shortest walk never repeats a node, so the simple
    paths contain all of them. No Dijkstra and no distance array.
    """
    adj = adjacency(n, edges)
    best = float("inf")
    on: List[bool] = [False] * len(edges)
    stack = [(0, 0, 1, ())]
    while stack:
        u, cost, seen, used = stack.pop()
        if u == n - 1:
            if cost < best:
                best = cost
                on = [False] * len(edges)
            if cost == best:
                for i in used:
                    on[i] = True
            continue
        for v, w, i in adj[u]:
            if not seen >> v & 1:
                stack.append((v, cost + w, seen | 1 << v, used + (i,)))
    return on


class Solution:
    def findAnswer(self, n: int, edges: List[List[int]]) -> List[bool]:
        """One Dijkstra from 0 and a walk back from n-1 over tight edges.

        The two-Dijkstra form and the programs that get it wrong are compared in `__main__`.
        """
        return walk_back(n, edges, adjacency(n, edges), tight)


def graphs(n: int, weights: Tuple[int, ...]):
    """Every simple graph on 0..n-1 with weights from `weights`, connected or not."""
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product((0,) + weights, repeat=len(pairs)):
        yield [[u, v, w] for (u, v), w in zip(pairs, choice) if w]


def random_graph(rng: random.Random, n: int, m: int, top: int) -> List[List[int]]:
    edges = {}
    target = min(m, n * (n - 1) // 2)
    while len(edges) < target:
        u, v = rng.sample(range(n), 2)
        edges.setdefault((min(u, v), max(u, v)), rng.randint(1, top))
    return [[u, v, w] for (u, v), w in edges.items()]


PROGRAMS = ("walk tight", "walk closer", "every tight", "parent", "parent flipped")


def run(n, edges) -> Dict[str, List[bool]]:
    adj = adjacency(n, edges)
    return {
        "two sided": two_sided(n, edges, adj),
        "walk tight": walk_back(n, edges, adj, tight),
        "walk closer": walk_back(n, edges, adj, closer),
        "every tight": every_tight_edge(n, edges, adj),
        "parent": parent_chain(n, edges, adj),
        "parent flipped": parent_chain(n, edges, adj, flip=True),
    }


def compare(got, truth) -> str:
    """'ok', 'over' (marks a superset), 'under' (a subset) or 'both'."""
    extra = any(g and not t for g, t in zip(got, truth))
    missing = any(t and not g for g, t in zip(got, truth))
    return {(False, False): "ok", (True, False): "over", (False, True): "under"}.get((extra, missing), "both")


if __name__ == "__main__":
    rng = random.Random(3123)
    started = time.time()

    print("== exhaustive: every simple graph, 0 to n-1 reachable or not ==")
    for n, weights in ((3, (1, 2, 3)), (4, (1, 2, 3)), (5, (1, 2))):
        total = reachable = several = 0
        tally = {p: {"ok": 0, "over": 0, "under": 0, "both": 0} for p in PROGRAMS}
        parents_differ = 0
        for edges in graphs(n, weights):
            total += 1
            truth = oracle(n, edges)
            got = run(n, edges)
            assert got["two sided"] == truth
            reachable += any(truth)
            # more than one shortest path is exactly when the marked edges are more than a path's worth
            marked = sum(truth)
            chain = sum(got["parent"])
            several += marked > chain
            for p in PROGRAMS:
                tally[p][compare(got[p], truth)] += 1
            parents_differ += got["parent"] != got["parent flipped"]
        assert tally["walk tight"]["ok"] == total
        print(f"  n={n} weights={weights}  graphs {total}  reachable {reachable}  more than one shortest path {several}"
              f"   parent edge sets differ by tie-break {parents_differ}")
        for p in PROGRAMS:
            t = tally[p]
            print(f"      {p:15s} wrong {total - t['ok']:6d}   over {t['over']:6d}   under {t['under']:6d}   both {t['both']:6d}")

    print("\n== random graphs, n = 10 ==")
    for m, top in ((12, 1), (12, 5), (25, 1), (25, 5), (25, 100)):
        tally = {p: 0 for p in PROGRAMS}
        several = 0
        for _ in range(1000):
            edges = random_graph(rng, 10, m, top)
            truth = oracle(10, edges)
            got = run(10, edges)
            assert got["two sided"] == truth and got["walk tight"] == truth
            several += sum(truth) > sum(got["parent"])
            for p in PROGRAMS:
                tally[p] += got[p] != truth
        print(f"  m={m:3d} top={top:3d}  more than one shortest path {several:4d}/1000   "
              + "   ".join(f"{p} wrong {tally[p]:4d}" for p in PROGRAMS))

    print("\n== the statement's size, timed ==")
    s = Solution()
    for n, m, top in ((50000, 50000, 100000), (50000, 50000, 1), (50000, 49999, 1)):
        edges = random_graph(rng, n, m, top)
        t0 = time.time()
        answer = s.findAnswer(n, edges)
        took = time.time() - t0
        assert answer == two_sided(n, edges, adjacency(n, edges))
        print(f"  n={n} m={len(edges)} top={top}  marked {sum(answer):6d}   {took:.2f}s")
    # a grid of unit edges, where every monotone lattice path is shortest and every edge is on one
    side = 158
    n = side * side
    edges = [[r * side + c, r * side + c + 1, 1] for r in range(side) for c in range(side - 1)]
    edges += [[r * side + c, (r + 1) * side + c, 1] for r in range(side - 1) for c in range(side)]
    t0 = time.time()
    answer = s.findAnswer(n, edges)
    took = time.time() - t0
    chain = parent_chain(n, edges, adjacency(n, edges))
    assert all(answer)
    print(f"  grid {side}x{side} m={len(edges)}  marked {sum(answer)} of {len(edges)}   parent chain marks {sum(chain)}   {took:.2f}s")

    print(f"\n{time.time() - started:.0f}s")
