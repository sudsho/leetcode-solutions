from typing import List


class DSU:
    """Disjoint sets over `1..n`, union by size. Undirected reachability only.

    The directedness of the input is not in here. That is deliberate: this
    structure answers "does adding this edge close an undirected cycle", and the
    in-degree bookkeeping that makes the graph directed is handled separately in
    `findRedundantDirectedConnection`. Mixing the two was the first version and
    it made the case analysis impossible to read.
    """

    def __init__(self, n: int):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        """Merge and report True, or report False if `a` and `b` already agree."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def is_rooted_tree(n: int, edges: List[List[int]]) -> bool:
    """True iff `edges` on nodes `1..n` form a tree rooted at some node.

    The definition the problem uses: exactly one node with in-degree 0, every
    other node with in-degree 1, and all nodes reachable from the root. With
    `n - 1` edges the reachability check subsumes acyclicity, so there is no
    separate cycle test.

    This is the specification, and it is here rather than in the test file
    because the fast routine below does not evaluate it even once. Keeping the
    two side by side is what turned up the case-A multiplicity.
    """
    if len(edges) != n - 1:
        return False
    indeg = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    for u, v in edges:
        indeg[v] += 1
        children[u].append(v)
    roots = [v for v in range(1, n + 1) if indeg[v] == 0]
    if len(roots) != 1 or any(indeg[v] > 1 for v in range(1, n + 1)):
        return False
    seen = {roots[0]}
    stack = [roots[0]]
    while stack:
        u = stack.pop()
        for v in children[u]:
            if v in seen:
                return False
            seen.add(v)
            stack.append(v)
    return len(seen) == n


def all_valid_removals(edges: List[List[int]]) -> List[int]:
    """Indices of every edge whose removal leaves a rooted tree. O(n^2).

    Not used by the solution. It exists because the answer to this problem is a
    choice out of this set, and the set is the only thing that says how big the
    choice actually is. Every published account of the problem I have read
    describes the ambiguity as "there may be two candidates"; run this on a pure
    directed cycle and it returns all of them.
    """
    n = len(edges)
    return [
        i
        for i in range(n)
        if is_rooted_tree(n, [e for j, e in enumerate(edges) if j != i])
    ]


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        """Remove one edge so that what is left is a rooted tree.

        The input is a rooted tree on `n` nodes plus one extra directed edge, so
        `n` nodes and `n` edges. Return an edge whose removal leaves a rooted
        tree; if more than one edge qualifies, return the one that appears last
        in `edges`.

        Picked to attack the rule the log has been circling for a week, which by
        last night read: a printed choice off a class is free exactly when the
        printed function factors through the quotient. Every problem it has been
        tested on - 711, 721, 1061, 1202 - answered the question structurally,
        and I wanted one where the structure declines to. This is that problem,
        and the tell is syntactic and sits in the statement itself: "if there are
        multiple answers, return the answer that occurs last in the input". The
        graph is the same object under any reordering of `edges`; the answer is
        not. So the printed function does not factor through the quotient, and no
        argument is owed anyway, because the statement legislated the tie rather
        than leaving it to be discovered. The "only if" half of the rule does not
        survive that, and neither do the four axes before it - all five were
        looking for a structural reason a choice is free, and stipulation is a
        non-structural one.

        Three nights running the log has said the pairs are a presentation and
        only the quotient survives. Here the presentation is the answer.

        The algorithm, and the tie-break is inside it rather than beside it:

          - a rooted tree has every in-degree 1 except the root's. `n` edges over
            `n` nodes means either exactly one node has in-degree 2, or none does
            and there is a directed cycle. Those are the two cases;
          - two parents. Call the edges `first` and `second` by input position.
            One of them must go. Try `second` first: union the others and see
            whether a cycle appears. If none does, `second` is an answer, and it
            is the later one, so it is *the* answer whether or not `first` also
            works. If a cycle does appear, `first` is on it and `second` is the
            only answer;
          - no two-parent node. Every in-degree is 1, the graph is connected, so
            there is exactly one directed cycle and every edge on it is an
            answer. Union in input order and return the first edge that closes a
            cycle - it is the last cycle edge to be scanned, so it is the last in
            input order.

        The order of the two trials in case B is not an implementation detail. If
        `first` is tried first it wins whenever both work, and both do work
        whenever the two-parent node is off the cycle, so the routine would
        return a legitimate edge and the wrong one. The statement's convention is
        compiled into the control flow at that line, which is a nicer answer than
        the one I expected to write, since the usual reading is that the trial
        order is arbitrary and only correctness of the case split matters.

        `O(n * alpha(n))` time, `O(n)` space.
        """
        n = len(edges)
        parent = [0] * (n + 1)
        first = second = -1
        for i, (u, v) in enumerate(edges):
            if parent[v]:
                first, second = parent[v] - 1, i
                # only one node can have two parents here, so there is nothing
                # to gain by continuing to look, but the scan is O(n) either way
                # and stopping early would need the loop split in two.
            else:
                parent[v] = i + 1

        dsu = DSU(n)
        for i, (u, v) in enumerate(edges):
            if i == second:
                continue
            if not dsu.union(u, v):
                # a cycle among everything except `second`. in case B that means
                # `first` is the edge on it; in case A `second` is -1, nothing
                # was skipped, and this edge is the one that closed the cycle.
                return edges[first] if second != -1 else edges[i]

        # no cycle without `second`, so removing `second` works. it is also the
        # later of the two candidates by construction, which is the whole reason
        # it is tried first.
        return edges[second]


if __name__ == "__main__":
    solution = Solution()

    # (edges, expected). the last three are the ones worth having: a 3-cycle
    # where all three edges are valid answers, a two-parent node off the cycle
    # where both candidates are valid, and a two-parent node on it where only
    # one is.
    cases = [
        ([[1, 2], [1, 3], [2, 3]], [2, 3]),
        ([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]], [4, 1]),
        ([[2, 1], [3, 1], [4, 2], [1, 4]], [2, 1]),
        ([[1, 2], [2, 3], [3, 1]], [3, 1]),
        ([[4, 2], [1, 4], [3, 1], [1, 3]], [1, 3]),
        ([[3, 1], [2, 3], [1, 2], [1, 4]], [1, 2]),
    ]
    for edges, expected in cases:
        got = solution.findRedundantDirectedConnection([e[:] for e in edges])
        valid = all_valid_removals(edges)
        # the point of the run: report how many answers were legal, not only
        # which one came back. the fast routine never computes this set.
        print(
            f"{str(edges):<42} -> {str(got):<8} expected {str(expected):<8}"
            f" {'ok' if got == expected else 'FAIL'}"
            f"   |valid|={len(valid)} at {valid}"
        )
        assert got == expected, (edges, got, expected)
        assert edges.index(got) == valid[-1], "not the last valid edge in input order"
