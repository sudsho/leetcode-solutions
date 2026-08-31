from typing import List

# Rows and columns are unioned in one structure, so the two coordinate families
# need disjoint labels. Coordinates are bounded by 1e4, so `~c` (negative) can
# never collide with a row label. The alternative, offsetting by a constant,
# works too and hides the fact that the two families are genuinely different
# kinds of thing; the bitwise complement does not.
def col_label(c: int) -> int:
    return ~c


class DSU:
    """Disjoint sets over arbitrary hashable labels, union by size."""

    def __init__(self):
        self.parent = {}
        self.size = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.size[x] = 1
            return x
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        """Maximum stones removable, where a stone may go if it shares a row or
        column with a stone still on the board.

        The answer is `n - c` for `c` the number of connected components of the
        "shares a row or column" graph, and the reason to write this one down
        next to 1202 is that it is the opposite kind of answer. 1202 asked for a
        representative of an orbit and the whole difficulty was choosing one.
        Here nothing is ever chosen: the quantity asked for is a function of the
        partition alone, so the quotient is the entire answer and no section is
        formed anywhere in the code or in the argument.

        That shows up concretely. Each component of `k` stones leaves exactly one
        stone behind, and *which* one is unconstrained - take any spanning tree of
        the component and peel leaves inward, and the root can be any vertex you
        like. So there are `k` distinct optimal plays per component and the
        answer cannot see the difference between them. A problem whose answer is
        a quotient invariant is allowed to be that indifferent; 1202's could not
        be, because its answer *was* the choice.

        Both halves of `n - c`:

        - at most `n - c`: the components are read off the *original* board and
          then held fixed, and no component can be emptied. A stone is legal to
          remove only while some other stone shares its row or column, and every
          such stone is in its own original component, so the last survivor of a
          component is frozen. `c` stones remain no matter how the moves are
          ordered - the bound needs no exchange argument, only an invariant.
        - at least `n - c`: spanning tree, remove leaves. A leaf always has a
          neighbour still present, which is precisely the legality condition.

        The implementation has a second quotient in it, and it is the part that
        makes this cheap. Building the stone graph directly is `O(n^2)` pairwise
        comparisons. Instead union the *labels* - stone `(r, c)` merges row `r`
        with column `c` - so the vertex set is the at most `2n` occupied lines
        rather than the stones, and every stone contributes one union instead of
        `n` comparisons. Two stones share a line iff their labels land in the same
        class, so components of the label graph and components of the stone graph
        agree, and counting distinct roots over the stones' rows recovers `c`.

        `O(n alpha(n))` time, `O(n)` space.
        """
        dsu = DSU()
        for r, c in stones:
            dsu.union(r, col_label(c))

        # count components *of the stones*, not of the label structure. an
        # isolated row label with no stone on it cannot occur here since every
        # label is introduced by a stone, but counting over the stones keeps that
        # independent of how find() populates the dictionaries.
        roots = {dsu.find(r) for r, _ in stones}
        return len(stones) - len(roots)
