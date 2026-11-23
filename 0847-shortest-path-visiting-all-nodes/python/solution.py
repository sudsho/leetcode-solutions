import itertools
import random
import time
from collections import deque
from typing import List


def popcount(m):
    """How many nodes a mask has visited. The count bar and the count mark keep only this number of a mask."""
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


def count_bar(graph, starts=None, fan=None):
    """One number per node, the most nodes any queued arrival had visited. 864's count bar, and wrong there.

    With `fan`, fan[u] is raised to the most pushes one pop of u got past the
    bar. A pop that queues one push or none queues the same thing whatever
    order u's list is in, so a node whose fan stays under 2 on every run
    cannot be what the adjacency order moves.
    """
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
        kept = 0
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            c = popcount(nm)
            if c > best[w]:
                best[w] = c
                queue.append((w, nm, d + 1))
                kept += 1
        if fan is not None and kept > fan[u]:
            fan[u] = kept
    return -1


def to_full(graph):
    """far[u][mask]: the fewest moves from standing at u having visited mask to having visited every node.

    Masks are done from the full one down. A move that adds a node lands on a
    larger mask, already done; a move inside the mask stays on it, so each
    mask is relaxed against itself until nothing changes. Masks without u are
    left at n * n, which no real state reaches.
    """
    n = len(graph)
    full = (1 << n) - 1
    big = n * n
    far = [[big] * (1 << n) for _ in range(n)]
    for u in range(n):
        far[u][full] = 0
    for m in sorted(range(1, full), key=popcount, reverse=True):
        inside = [u for u in range(n) if m >> u & 1]
        for u in inside:
            far[u][m] = min([1 + far[w][m | 1 << w] for w in graph[u] if not m >> w & 1] + [big])
        changed = True
        while changed:
            changed = False
            for u in inside:
                for w in graph[u]:
                    if 1 + far[w][m] < far[u][m]:
                        far[u][m] = 1 + far[w][m]
                        changed = True
    return far


def count_meets(graph, starts=None, fan=None, meet=None, pair=None, far=None, gap=None):
    """The count bar with a parent for every queued arrival, recording where two lines of descent meet at a bar.

    Arrivals at one node at different depths are popped in depth order
    whatever the lists say, so the order can only act where a push at x finds
    the bar last set by another arrival at the same depth. That pair's queue
    order was fixed at the pop where their lines split, by that node's list
    alone. meet[(kind, node)] counts those meetings, kind "tie" where the push
    has the same count as the bar, "under" and "over" otherwise, node -1 where
    the two lines go back to different starts and the start order fixed it.
    With `pair`, every tie is also counted under (same mask?, split node): a
    tie between two arrivals with one mask keeps the same state whichever
    of them the order lets in. With `far` (from to_full) and `gap`, every
    tie between different masks is counted under (which is nearer full,
    split node): 0 when the kept and the refused mask are equally far from
    full at that node, 1 when the kept one is nearer, -1 when the refused one
    is, the only case where letting the other in could have finished sooner.
    """
    n = len(graph)
    if n == 1:
        return 0
    full = (1 << n) - 1
    best = [0] * n
    setter = [-1] * n
    parent, node_of, depth_of, mask_of = [], [], [], []
    queue = deque()
    for u in (range(n) if starts is None else starts):
        best[u] = 1
        setter[u] = len(parent)
        parent.append(-1)
        node_of.append(u)
        depth_of.append(0)
        mask_of.append(1 << u)
        queue.append((u, 1 << u, 0, setter[u]))
    while queue:
        u, mask, d, me = queue.popleft()
        kept = 0
        for w in graph[u]:
            nm = mask | 1 << w
            if nm == full:
                return d + 1
            c = popcount(nm)
            s = setter[w]
            if meet is not None and s >= 0 and depth_of[s] == d + 1:
                a, b = me, parent[s]
                while a != b and a >= 0:
                    a, b = parent[a], parent[b]
                kind = "tie" if c == best[w] else "under" if c < best[w] else "over"
                key = (kind, node_of[a] if a >= 0 else -1)
                meet[key] = meet.get(key, 0) + 1
                if pair is not None and kind == "tie":
                    pk = (nm == mask_of[s], key[1])
                    pair[pk] = pair.get(pk, 0) + 1
                    if gap is not None and not pk[0]:
                        kf, rf = far[w][mask_of[s]], far[w][nm]
                        gk = (0 if kf == rf else 1 if kf < rf else -1, key[1])
                        gap[gk] = gap.get(gk, 0) + 1
            if c > best[w]:
                best[w] = c
                setter[w] = len(parent)
                parent.append(me)
                node_of.append(w)
                depth_of.append(d + 1)
                mask_of.append(nm)
                queue.append((w, nm, d + 1, setter[w]))
                kept += 1
        if fan is not None and kept > fan[u]:
            fan[u] = kept
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
    """Whether a DFS from node 0 reaches every node. 847 promises a connected graph, so `exhaustive` skips the rest."""
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


def cut_vertices(graph):
    """Nodes whose removal disconnects the rest, by a DFS from a remaining node with the node taken out."""
    n = len(graph)
    out = set()
    for u in range(n):
        rest = 1 if u == 0 else 0
        seen, stack = {rest}, [rest]
        while stack:
            x = stack.pop()
            for w in graph[x]:
                if w != u and w not in seen:
                    seen.add(w)
                    stack.append(w)
        if len(seen) < n - 1:
            out.add(u)
    return out


def edges_of(graph):
    """Each edge once as "u-w" with u < w, the form the printed witnesses use."""
    return " ".join(f"{u}-{w}" for u in range(len(graph)) for w in graph[u] if u < w)


def decides(keys, rows):
    """Whether orders that share a key always share a row, so the key is all of the order the row needs."""
    seen = {}
    return all(seen.setdefault(k, r) == r for k, r in zip(keys, rows))


def fewest_nodes(views, rows, n):
    """The fewest nodes whose entries in each view decide the row; n + 1 if all n together do not."""
    for k in range(n + 1):
        for nodes in itertools.combinations(range(n), k):
            if decides([tuple(v[u] for u in nodes) for v in views], rows):
                return k
    return n + 1


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

    # why the count bar's wrong count is pinned at n <= 5. first per graph:
    # does the adjacency order alone ever change its answer? then per
    # isomorphism class: does each class hold its own count under every order,
    # or do the classes trade wrong graphs and only the total hold still?
    print("\n== the pinned count, per graph and per isomorphism class ==")
    prng = random.Random(8470)
    for n in (5, 6):
        pairs = list(itertools.combinations(range(n), 2))
        idx = {p: i for i, p in enumerate(pairs)}
        perms = list(itertools.permutations(range(n)))
        pmaps = [[idx[tuple(sorted((p[a], p[b])))] for a, b in pairs] for p in perms]
        orders = perms if n <= 5 else [tuple(range(n))] + prng.sample(perms, 59)
        per_class, copies, moves, reps = {}, {}, 0, {}
        for graph, m in exhaustive(n):
            bits = [i for i, (a, b) in enumerate(pairs) if b in graph[a]]
            canon = min(sum(1 << pm[i] for i in bits) for pm in pmaps)
            want = layered(graph)
            reps.setdefault(canon, (graph, want))
            outs = [count_bar(reorder(graph, o)) for o in orders]
            moves += len(set(outs)) > 1
            row = per_class.setdefault(canon, [0] * len(orders))
            copies[canon] = copies.get(canon, 0) + 1
            for k, got in enumerate(outs):
                row[k] += got != want
        totals = [sum(r[k] for r in per_class.values()) for k in range(len(orders))]
        moving = [c for c, r in per_class.items() if len(set(r)) > 1]
        print(f"  n = {n}, {len(orders)} adjacency orders: the order changes the answer on {moves} graphs,"
              f" totals {min(totals)} to {max(totals)} (default {totals[0]}),"
              f" classes {len(per_class)}, {sum(1 for r in per_class.values() if r[0] and len(set(r)) == 1)} wrong and pinned,"
              f" {len(moving)} move, default the worst on {sum(per_class[c][0] == max(per_class[c]) for c in moving)}")

    # what pins a class. summing over a class's labellings averages the
    # member's answer over adjacency orders a and start orders b together, so
    # if wrongness on one member is g(a) + h(b) each part averages to a
    # constant and the class cannot move. split each n = 6 class by how its
    # representative's wrongness depends on (a, b) over 40 x 40 pairs.
    print("\n== what pins a class: one member under 40 adjacency orders x 40 start orders, n = 6 ==")
    oa = [tuple(range(6))] + random.Random(1).sample(perms, 39)
    ob = [tuple(range(6))] + random.Random(2).sample(perms, 39)
    split, sym, full, pairs_of, gaps_of = {}, {}, {}, {}, {}
    for canon, (graph, want) in reps.items():
        f = [[int(count_bar(reorder(graph, a), b) != want) for b in ob] for a in oa]
        a_only = all(r[j] == r[0] for r in f for j in range(len(ob)))
        b_only = all(f[i][j] == f[0][j] for i in range(len(oa)) for j in range(len(ob)))
        additive = all(f[i][j] - f[i][0] - f[0][j] + f[0][0] == 0 for i in range(len(oa)) for j in range(len(ob)))
        kind = ("neither" if a_only and b_only else "adjacency only" if a_only else "start only" if b_only
                else "additive" if additive else "joint")
        key = ("moves" if canon in moving else "pinned", kind)
        split[key] = split.get(key, 0) + 1
        # the class's symmetry, and how much of the grid the interaction covers:
        # the double centring of f, f - row mean - column mean + grand mean
        bits = {i for i, (a, b) in enumerate(pairs) if b in graph[a]}
        aut = sum(1 for pm in pmaps if {pm[i] for i in bits} == bits)
        rows = [sum(r) / len(ob) for r in f]
        cols = [sum(f[i][j] for i in range(len(oa))) / len(oa) for j in range(len(ob))]
        grand = sum(rows) / len(oa)
        inter = sum((f[i][j] - rows[i] - cols[j] + grand) ** 2 for i in range(len(oa)) for j in range(len(ob)))
        total_var = sum((f[i][j] - grand) ** 2 for i in range(len(oa)) for j in range(len(ob)))
        # is the member wrong on an exclusive-or of one fact about a and one about
        # b? then every row is some one row or its complement. exactly, and the
        # share of the grid the best such pattern gets right
        exact = all(f[i][j] ^ f[i][0] ^ f[0][j] ^ f[0][0] == 0 for i in range(len(oa)) for j in range(len(ob)))
        fit = max(sum(max(agree, len(ob) - agree) for agree in (sum(x == y for x, y in zip(r, ref)) for r in f))
                  for ref in f) / (len(oa) * len(ob))
        # which facts about the adjacency order pick the row. the search only
        # sees the reordered lists, so those decide it by construction; is the
        # first neighbour in each list enough, and at how many nodes?
        rows = [tuple(r) for r in f]
        lists = [tuple(tuple(adj) for adj in reorder(graph, a)) for a in oa]
        firsts = [tuple(adj[0] for adj in g2) for g2 in lists]
        sym.setdefault(key, []).append((aut, inter / total_var if total_var else 0.0, grand, exact, fit,
                                        len(set(rows)), len(set(lists)), len(set(firsts)),
                                        decides(firsts, rows), fewest_nodes(lists, rows, 6),
                                        fewest_nodes(firsts, rows, 6)))
        # the same count over all 720 orders, where every pair of lists repeats
        # often enough to be tested. the row is a function of the lists, so one
        # run per distinct set of lists. then which nodes: is some smallest
        # deciding set the highest-degree nodes?
        by_lists = {}
        fan = [0] * 6
        meet, pair, gap = {}, {}, {}
        far = to_full(graph)      # reorder keeps the labels, so one table serves every order
        for a in perms:
            g2 = tuple(tuple(adj) for adj in reorder(graph, a))
            if g2 not in by_lists:
                by_lists[g2] = tuple(int(count_meets(g2, b, fan, meet, pair, far, gap) != want) for b in ob)
        views, all_rows = list(by_lists), list(by_lists.values())
        k = fewest_nodes(views, all_rows, 6)
        deg = sorted((len(adj) for adj in graph), reverse=True)
        sets = [nodes for nodes in itertools.combinations(range(6), k)
                if decides([tuple(v[u] for u in nodes) for v in views], all_rows)]
        top = any(sorted((len(graph[u]) for u in nodes), reverse=True) == deg[:k] for nodes in sets)
        # where they are not the busiest: is a deciding set always found among
        # the nodes on a cycle (two neighbours or more and not a cut vertex),
        # and is the busiest node left out of every deciding set?
        cuts = cut_vertices(graph)
        on_cycle = {u for u in range(6) if len(graph[u]) >= 2 and u not in cuts}
        busiest = {u for u in range(6) if len(graph[u]) == deg[0]}
        inside = any(set(nodes) <= on_cycle for nodes in sets)
        hub_out = not any(busiest & set(nodes) for nodes in sets)
        # why a hub's list stops mattering: does the hub ever get two pushes
        # past the bar at one pop, over every list order and start order run?
        # under 2 it provably cannot matter; the question is whether that is
        # the whole reason. and the converse at every node: is a node with a
        # fan of 2 or more always in some smallest deciding set?
        used = set().union(*map(set, sets)) if sets else set()
        wide = {u for u in range(6) if fan[u] >= 2}
        # do the two pushes' lines ever meet at a bar at equal depth, and where
        # do they split? a node whose list decides the row must be the split
        # of some meeting, since that is the only place an order acts. is it
        # the ties, same count at same depth, that pick the deciding nodes?
        feed = {u for (kind, u) in meet if u >= 0}
        feed_tie = {u for (kind, u) in meet if kind == "tie" and u >= 0}
        n_meet = sum(meet.values())
        n_tie = sum(c for (kind, u), c in meet.items() if kind == "tie")
        n_root = sum(c for (kind, u), c in meet.items() if u < 0)
        # are the hub's ties between equal masks? a tie keeps one of two
        # arrivals with the same count; if both carry the same mask the state
        # is the same whichever is kept. split the tie splits by that.
        split_diff = {u for (eq, u) in pair if not eq and u >= 0}
        n_same = sum(c for (eq, u), c in pair.items() if eq)
        hub_ties = [(eq, c) for (eq, u), c in pair.items() if u in busiest]
        hub_same = sum(c for eq, c in hub_ties if eq) / max(1, sum(c for _, c in hub_ties))
        pairs_of.setdefault(key, []).append((split_diff == used, len(split_diff - used), len(used - split_diff),
                                             n_same / n_tie if n_tie else 0.0, hub_out, hub_same,
                                             hub_out and not any(not eq for eq, _ in hub_ties)))
        # are the two masks of an unequal tie the same distance from full? a
        # refused mask can only cost the answer if it was nearer full than the
        # kept one, so the splits of those ties should be the deciding nodes,
        # and the idle hub's unequal ties should all be at equal distance.
        n_gap = sum(gap.values())
        near_split = {u for (g, u) in gap if g < 0 and u >= 0}
        hub_gap = [(g, c) for (g, u), c in gap.items() if u in busiest]
        hub_eq = sum(c for g, c in hub_gap if g == 0) / max(1, sum(c for _, c in hub_gap))
        gaps_of.setdefault(key, []).append((
            sum(c for (g, u), c in gap.items() if g == 0) / n_gap if n_gap else 0.0,
            sum(c for (g, u), c in gap.items() if g > 0) / n_gap if n_gap else 0.0,
            sum(c for (g, u), c in gap.items() if g < 0) / n_gap if n_gap else 0.0,
            near_split == used, len(near_split - used), len(used - near_split),
            hub_out, hub_out and all(g == 0 for g, _ in hub_gap), hub_eq,
            hub_out and not any(g < 0 for g, _ in hub_gap)))
        full.setdefault(key, []).append((len(views), len(set(all_rows)), k, sum(d >= 2 for d in deg), top, len(sets),
                                         inside, hub_out, bool(busiest & cuts), max(fan[u] for u in busiest),
                                         len(used - wide), len(wide - used), len(wide), wide == used,
                                         len(used - feed), feed == used, feed_tie == used, n_tie > 0,
                                         n_tie / n_meet if n_meet else 0.0, n_root / n_meet if n_meet else 0.0,
                                         hub_out and bool(busiest & feed), len(feed - used), len(feed_tie - used)))
    for (state, kind), c in sorted(split.items()):
        auts = sorted(s[0] for s in sym[(state, kind)])
        share = sum(s[1] for s in sym[(state, kind)]) / c
        rate = sum(s[2] for s in sym[(state, kind)]) / c
        print(f"  {state:6s}  {kind:14s} {c:3d} classes   |Aut| median {auts[c // 2]:3d}, 1 on {auts.count(1):2d},"
              f" interaction share of the variance {share:.2f}, wrong on {rate:.2f} of the grid")
        got = sym[(state, kind)]
        print(f"          exclusive-or exactly on {sum(g[3] for g in got):2d}, best exclusive-or pattern right on"
              f" {sum(g[4] for g in got) / c:.2f} of the grid (least {min(g[4] for g in got):.2f}),"
              f" distinct rows median {sorted(g[5] for g in got)[c // 2]} of {len(oa)}")
        ok = [g for g in got if g[8]]
        print(f"          distinct list orders median {sorted(g[6] for g in got)[c // 2]}, distinct first-neighbour"
              f" tuples median {sorted(g[7] for g in got)[c // 2]}, the firsts decide the row on {len(ok):2d},"
              f" fewest nodes whose lists decide it: median {sorted(g[9] for g in got)[c // 2]}, most {max(g[9] for g in got)}"
              + (f", whose firsts do, where they do: median {sorted(g[10] for g in ok)[len(ok) // 2]}" if ok else ""))
        al = full[(state, kind)]
        print(f"          all 720 orders: distinct list orders median {sorted(g[0] for g in al)[c // 2]}, distinct rows median"
              f" {sorted(g[1] for g in al)[c // 2]}, fewest nodes whose lists decide the row: median {sorted(g[2] for g in al)[c // 2]},"
              f" most {max(g[2] for g in al)}, every node with two neighbours or more on {sum(g[2] == g[3] for g in al):2d},"
              f" the highest-degree nodes are such a set on {sum(g[4] for g in al):2d}, one set only on {sum(g[5] == 1 for g in al):2d}")
        for label, part in (("where they are", [g for g in al if g[4]]), ("where they are not", [g for g in al if not g[4]])):
            if part:
                print(f"          {label:18s} ({len(part):2d}): a deciding set on the cycle nodes on {sum(g[6] for g in part):2d},"
                      f" the busiest node in none on {sum(g[7] for g in part):2d}, the busiest a cut vertex on {sum(g[8] for g in part):2d}")
                out = [g for g in part if g[7]]
                print(f"          {'':18s}       the busiest under two pushes a pop on {sum(g[9] < 2 for g in part):2d}"
                      f" ({sum(g[9] < 2 for g in out):2d} of the {len(out):2d} where it is in none),"
                      f" busiest fan median {sorted(g[9] for g in part)[len(part) // 2]}")
        print(f"          fan 2 or more at a node: deciding nodes with a fan under 2 {sum(g[10] for g in al)} (must be 0),"
                  f" wide nodes in no smallest deciding set on {sum(g[11] > 0 for g in al):2d} classes ({sum(g[11] for g in al)} nodes"
                  f" of {sum(g[12] for g in al)}), wide nodes exactly the deciding nodes on {sum(g[13] for g in al):2d}")
        print(f"          meetings at equal depth: deciding nodes that split none {sum(g[14] for g in al)} (must be 0),"
              f" ties on {sum(g[17] for g in al):2d} classes, {sum(g[18] for g in al) / c:.2f} of meetings ties,"
              f" {sum(g[19] for g in al) / c:.2f} back to two starts")
        print(f"          {'':18s} splits exactly the deciding nodes on {sum(g[15] for g in al):2d} ({sum(g[21] for g in al)} extra),"
              f" tie splits exactly them on {sum(g[16] for g in al):2d} ({sum(g[22] for g in al)} extra),"
              f" an idle hub splits a meeting on {sum(g[20] for g in al):2d} of {sum(g[7] for g in al):2d}")
        pp = pairs_of[(state, kind)]
        idle = [g for g in pp if g[4]]
        print(f"          ties between equal masks {sum(g[3] for g in pp) / c:.2f} of ties, splits of unequal ties exactly"
              f" the deciding nodes on {sum(g[0] for g in pp):2d} ({sum(g[1] for g in pp)} extra,"
              f" {sum(g[2] for g in pp)} deciding nodes that split none), an idle hub's ties all equal masks on"
              f" {sum(g[6] for g in idle):2d} of {len(idle):2d}"
              + (f", equal on {sum(g[5] for g in idle) / len(idle):.2f} of its ties" if idle else ""))
        gg = gaps_of[(state, kind)]
        idle = [g for g in gg if g[6]]
        print(f"          unequal ties, distance to full: equal {sum(g[0] for g in gg) / c:.2f}, kept nearer"
              f" {sum(g[1] for g in gg) / c:.2f}, refused nearer {sum(g[2] for g in gg) / c:.2f}; splits of refused-nearer"
              f" ties exactly the deciding nodes on {sum(g[3] for g in gg):2d} ({sum(g[4] for g in gg)} extra,"
              f" {sum(g[5] for g in gg)} deciding nodes that split none), an idle hub's all equal distance on"
              f" {sum(g[7] for g in idle):2d} of {len(idle):2d}, none refused-nearer on {sum(g[9] for g in idle):2d}"
              + (f", equal on {sum(g[8] for g in idle) / len(idle):.2f} of its unequal ties" if idle else ""))

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
