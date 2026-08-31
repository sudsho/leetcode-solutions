from typing import List


class DSU:
    """Disjoint sets over `0..n-1`, union by size with path compression.

    The only thing this structure knows how to answer is "same class?", which is
    exactly the whole content of the problem: the edges in `pairs` are individual
    transpositions, but nothing below ever needs to know which transpositions
    were given, only which positions they connect. See `smallestStringWithSwaps`
    for why that is not a shortcut but a theorem.
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        """Lexicographically smallest string reachable by repeated given swaps.

        The reachable set is an orbit. Each pair `(i, j)` is a transposition of
        positions, "any number of times, in any order" is the group `G` they
        generate, and the strings reachable from `s` are `G . s`. So the answer
        is a *representative* of one orbit - a section of the quotient map, in
        the language of the last two days - and not the orbit itself.

        Two facts do all the work, and they are about different halves of that.

        **The group only remembers the components.** Transpositions along a
        connected graph on a vertex set `C` generate the full symmetric group on
        `C`: `(a b)` and `(b c)` give `(a c)` by conjugation, so connectivity
        propagates arbitrary swaps along any path. Hence `G = prod_C Sym(C)` over
        the connected components of the pair graph, and two different edge sets
        with the same components generate the *same* group. That is why a DSU is
        enough and why the input edges can be thrown away the moment they are
        merged - `pairs` is a presentation of `G`, and the components are `G`.

        A consequence worth stating because it is the part that surprises: within
        a component every rearrangement is available, and across components none
        is. So the orbit is the product over components of "all permutations of
        this component's multiset of characters", and its size is a product of
        multinomials - large, and never enumerated.

        **The order is supplied from outside and it factorises.** Picking the
        least element of the orbit needs an order on strings, and lex order is not
        `G`-equivariant (`G` permutes positions, which is exactly what lex order
        reads). It does not have to be: the min is taken within one orbit, which
        is a finite set, so it is well defined for the trivial reason. The
        distinction from a case where no order exists at all is that here the
        order is *given by the problem* rather than looked for - the section is
        what is being asked for, so there is nothing to justify.

        What does need an argument is that sorting each component independently
        gives the global minimum, since lex order does not obviously decompose.
        It does here: scan positions left to right, and at position `p` the
        characters that can be placed are precisely the unused ones from `p`'s
        component, unconstrained by any other component. Choosing anything but
        the smallest available is beaten by the string that swaps them, and that
        swap stays inside the orbit. So the greedy is an exchange argument one
        component at a time, and "sort the characters, write them back in
        increasing position order" is that greedy in closed form.

        `O(n alpha(n) + m + n log n)` time, `O(n)` space.
        """
        n = len(s)
        dsu = DSU(n)
        for i, j in pairs:
            dsu.union(i, j)

        # bucket positions by component. positions arrive in increasing order,
        # so each bucket is already sorted and only the characters need sorting.
        groups = {}
        for i in range(n):
            groups.setdefault(dsu.find(i), []).append(i)

        out = [""] * n
        for positions in groups.values():
            for pos, ch in zip(positions, sorted(s[i] for i in positions)):
                out[pos] = ch
        return "".join(out)
