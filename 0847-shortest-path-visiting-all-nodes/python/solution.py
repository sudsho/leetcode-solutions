import itertools
import random
import time
from collections import deque
from typing import List


def popcount(m):
    return bin(m).count("1")


def reorder(graph, order):
    """The same graph with each adjacency list sorted by order[w]."""
    return [sorted(adj, key=order.__getitem__) for adj in graph]


def layered(graph, counter=None, starts=None):
    """BFS on (node, mask of nodes visited) from every node at once, each state visited once. The textbook search."""
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    seen = bytearray(n << n)
    queue = deque()
    for u in (range(n) if starts is None else starts):
        seen[u << n | 1 << u] = 1
        queue.append((u, 1 << u, 0))
    while queue:
        u, mask, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            if not seen[w << n | nm]:
                seen[w << n | nm] = 1
                queue.append((w, nm, d + 1))
    return -1


def antichain_bar(graph, counter=None, widest=None, starts=None):
    """864's bar on a graph where every node is its own key: a set of masks per node, none a subset of another.

    A push at (node, mask) is dropped when a superset of mask has already been
    queued at the node. That arrival is no later, since every edge costs 1 and
    the bar goes on at the push, and it has everything this one has, so every
    walk this one could finish it can finish no later. A surviving push evicts
    the subsets it dominates. Every mask queued at u contains u, so the widest
    the set can be is C(n - 1, (n - 1) // 2).
    """
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    front = [[] for _ in range(n)]
    queue = deque()
    for u in (range(n) if starts is None else starts):
        front[u].append(1 << u)
        queue.append((u, 1 << u, 0))
    while queue:
        u, mask, d = queue.popleft()
        if counter is not None:
            counter[0] += 1
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            held = front[w]
            if any(m & nm == nm for m in held):
                continue
            held[:] = [m for m in held if m & nm != m]
            held.append(nm)
            if widest is not None and len(held) > widest[0]:
                widest[0] = len(held)
            queue.append((w, nm, d + 1))
    return -1


def count_bar(graph, starts=None):
    """One number per node, the most nodes any queued arrival had visited. 864's count bar, and wrong there."""
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    best = [0] * n
    queue = deque()
    for u in (range(n) if starts is None else starts):
        best[u] = 1
        queue.append((u, 1 << u, 0))
    while queue:
        u, mask, d = queue.popleft()
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            c = popcount(nm)
            if c > best[w]:
                best[w] = c
                queue.append((w, nm, d + 1))
    return -1


def count_mark(graph, starts=None):
    """One mark per (node, number of nodes visited): n^2 states instead of n 2^n, and two masks of one size are not the same mask."""
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    seen = bytearray(n * (n + 1))
    queue = deque()
    for u in (range(n) if starts is None else starts):
        seen[u * (n + 1) + 1] = 1
        queue.append((u, 1 << u, 0))
    while queue:
        u, mask, d = queue.popleft()
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            c = popcount(nm)
            if not seen[w * (n + 1) + c]:
                seen[w * (n + 1) + c] = 1
                queue.append((w, nm, d + 1))
    return -1


def one_mark(graph):
    """One visited mark per node. Every node is a start, so every node is marked before the first pop."""
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    seen = [True] * n
    queue = deque((u, 1 << u, 0) for u in range(n))
    while queue:
        u, mask, d = queue.popleft()
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            if not seen[w]:
                seen[w] = True
                queue.append((w, nm, d + 1))
    return -1


def oracle(graph):
    """Layers of (node, mask) with nothing marked visited, for as many layers as there are states."""
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    layer = {(u, 1 << u) for u in range(n)}
    for t in range(n << n):
        nxt = set()
        for u, mask in layer:
            for w in graph[u]:
                nm = mask | 1 << w
                if nm == full:
                    return t + 1
                nxt.add((w, nm))
        if not nxt:
            return -1
        layer = nxt
    return -1


class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        """BFS on (node, mask) from every node with a per-node antichain of masks as the bar. The rest is in `__main__`."""
        return antichain_bar(graph)


def connected(graph):
    n = len(graph)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for w in graph[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def exhaustive(n):
    """Every connected graph on n labelled nodes, as adjacency lists in ascending order, with its edge count."""
    pairs = list(itertools.combinations(range(n), 2))
    for bits in range(1 << len(pairs)):
        graph = [[] for _ in range(n)]
        m = 0
        for i, (a, b) in enumerate(pairs):
            if bits >> i & 1:
                graph[a].append(b)
                graph[b].append(a)
                m += 1
        if connected(graph):
            yield graph, m


def random_graph(rng, n, m):
    """A random tree on n nodes plus m - (n - 1) more edges at random."""
    edges = set()
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):
        a, b = nodes[i], nodes[rng.randrange(i)]
        edges.add((min(a, b), max(a, b)))
    pairs = [p for p in itertools.combinations(range(n), 2) if p not in edges]
    edges.update(rng.sample(pairs, m - (n - 1)))
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    return [sorted(adj) for adj in graph]


def edges_of(graph):
    return " ".join(f"{u}-{w}" for u in range(len(graph)) for w in graph[u] if u < w)


if __name__ == "__main__":
    rng = random.Random(847)
    started = time.time()

    for n in (3, 4, 5, 6):
        print(f"== every connected graph on {n} labelled nodes ==")
        perms = list(itertools.permutations(range(n)))
        sample = perms if n <= 5 else rng.sample(perms, 3)
        total = 0
        wrong = dict.fromkeys(["antichain bar", "count bar", "count mark", "one mark"], 0)
        by_adj = {"count bar": [0] * len(sample), "count mark": [0] * len(sample)}
        by_start = {"count bar": [0] * len(sample), "count mark": [0] * len(sample)}
        pops_l, pops_a, widest = [0], [0], [0]
        smallest = {}
        checked = 0
        answers = {}
        for graph, m in exhaustive(n):
            total += 1
            want = layered(graph, pops_l)
            answers[want] = answers.get(want, 0) + 1
            if n <= 5 or total % 7 == 0:
                checked += 1
                assert oracle(graph) == want, graph
            got = {
                "antichain bar": antichain_bar(graph, pops_a, widest),
                "count bar": count_bar(graph),
                "count mark": count_mark(graph),
                "one mark": one_mark(graph),
            }
            for name in wrong:
                if got[name] != want:
                    wrong[name] += 1
                    if name not in smallest or (m, want) < smallest[name][0]:
                        smallest[name] = ((m, want), graph, want, got[name])
            for i, order in enumerate(sample):
                g2 = reorder(graph, order)
                by_adj["count bar"][i] += count_bar(g2) != want
                by_adj["count mark"][i] += count_mark(g2) != want
                by_start["count bar"][i] += count_bar(graph, order) != want
                by_start["count mark"][i] += count_mark(graph, order) != want
        print(f"  graphs {total}   oracle agreed with layered on all {checked} checked"
              f"   answers: " + "  ".join(f"{a}: {c}" for a, c in sorted(answers.items())))
        for name in wrong:
            print(f"  {name:14s} wrong {wrong[name]:6d}   {100 * wrong[name] / total:.2f}%")
        for name, (key, graph, want, got) in smallest.items():
            print(f"    fewest edges for {name}: {edges_of(graph)}: {want}, it says {got}")
        for name in by_adj:
            print(f"  {name} by the adjacency order, {len(sample)} orders: best wrong {min(by_adj[name])}"
                  f" ({100 * min(by_adj[name]) / total:.2f}%), worst {max(by_adj[name])} ({100 * max(by_adj[name]) / total:.2f}%),"
                  f" distinct counts {len(set(by_adj[name]))}")
            print(f"  {name} by the start order:    best wrong {min(by_start[name])}"
                  f" ({100 * min(by_start[name]) / total:.2f}%), worst {max(by_start[name])} ({100 * max(by_start[name]) / total:.2f}%),"
                  f" distinct counts {len(set(by_start[name]))}")
        bound = len(list(itertools.combinations(range(n - 1), (n - 1) // 2)))
        print(f"  pops: layered {pops_l[0]}   antichain bar {pops_a[0]}   saved {100 * (1 - pops_a[0] / pops_l[0]):.1f}%"
              f"   widest antichain at a node {widest[0]} against C({n - 1}, {(n - 1) // 2}) = {bound}")

    print("\n== random connected graphs on 8 nodes, 2000 at each edge count ==")
    print("  edges   count bar   count mark   antichain wrong   pops saved   widest   bound 35")
    for m in (7, 9, 12, 16, 22, 28):
        wrong = dict.fromkeys(["antichain bar", "count bar", "count mark"], 0)
        pops_l, pops_a, widest = [0], [0], [0]
        for _ in range(2000):
            graph = random_graph(rng, 8, m)
            want = layered(graph, pops_l)
            wrong["antichain bar"] += antichain_bar(graph, pops_a, widest) != want
            wrong["count bar"] += count_bar(graph) != want
            wrong["count mark"] += count_mark(graph) != want
        print(f"  {m:5d}   {wrong['count bar']:5d} ({100 * wrong['count bar'] / 2000:4.1f}%)"
              f"   {wrong['count mark']:5d} ({100 * wrong['count mark'] / 2000:4.1f}%)        {wrong['antichain bar']}"
              f"         {100 * (1 - pops_a[0] / pops_l[0]):5.1f}%       {widest[0]:2d}")

    print("\n== the statement's size: 12 nodes, three graphs at each edge count, C(11, 5) = 462 ==")
    s = Solution()
    print("  edges   answer   layered pops      time   antichain pops      time   saved   widest")
    for m in (11, 14, 20, 30, 45, 66):
        for seed in range(3):
            graph = random_graph(random.Random(seed), 12, m)
            c1, c2, w = [0], [0], [0]
            t0 = time.time()
            a = layered(graph, c1)
            el1 = time.time() - t0
            t0 = time.time()
            b = antichain_bar(graph, c2, w)
            el2 = time.time() - t0
            assert a == b == s.shortestPathLength(graph)
            print(f"  {m:5d}   {a:6d}   {c1[0]:12d}   {el1:6.3f}s   {c2[0]:14d}   {el2:6.3f}s   {100 * (1 - c2[0] / max(1, c1[0])):5.1f}%   {w[0]:4d}"
                  f"   count bar {'right' if count_bar(graph) == a else 'wrong'}, count mark {'right' if count_mark(graph) == a else 'wrong'}")

    print(f"\n{time.time() - started:.0f}s")
