from typing import List


class SmallestRootDSU:
    """Disjoint sets over `0..n-1`, rooted at the *smallest* member of each class.

    The union rule is the one design decision in this file. The usual rule is
    union by size or rank, which keeps the trees shallow and leaves the root as
    whichever element happened to win; this one throws that away and always makes
    the smaller index the parent. See `smallestEquivalentString` for why, and for
    what it costs.
    """

    def __init__(self, n: int = 26):
        self.parent = list(range(n))

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
        # smaller root wins, unconditionally. this is what makes `find` return
        # the answer rather than an arbitrary label.
        if rb < ra:
            ra, rb = rb, ra
        self.parent[rb] = ra


class Solution:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        """Map each letter of `baseStr` to the smallest letter equivalent to it.

        `s1[i] ~ s2[i]` for every `i`, closed under reflexivity, symmetry and
        transitivity; return the lexicographically smallest string reachable from
        `baseStr` by replacing letters with equivalent ones.

        Picked to run the test the 721 entry left open. The rule as of last night
        was that a printed choice off a class is free exactly when the printed
        function factors through the quotient, and the point of writing that down
        was that it is checkable *before* any code. Here it is checkable in one
        line: what gets printed is `min` of the class, `min` is a function of the
        class and of nothing else, so it factors, so the choice is free. That is
        the prediction and it holds.

        What the problem is actually good for is that last night produced two
        phrasings of that rule and I treated them as the same statement:

          (a) a choice needs an argument when the observable part *varies* across
              the class;
          (b) a printed choice is free exactly when the printed function factors
              through the quotient.

        This separates them. The observable part varies about as hard as it can -
        a class here holds up to 26 different letters and telling them apart is
        the entire problem - so (a) says an argument is owed. None is. (b) is the
        one that survives, and (a) fails because it quietly assumed the thing
        printed is a *member* picked out of the class. `min` is not a member
        picked out; it is an aggregate over all of them, so the class is the
        argument rather than a bag of candidates to choose between. In 721 the
        name was constant on classes, which is the one case where picking a member
        and aggregating over the class agree, so the difference could not show up
        there and (a) got fitted to it.

        The other half is 1202 sitting right next to this. Same union-find, same
        phrase "lexicographically smallest" in the statement, and 1202 needed a
        real exchange argument while this needs none. The difference is not the
        group and not the order. In 1202 the output is a *joint* arrangement -
        a bijection from the class's positions to the class's characters - so the
        characters are a shared resource, choosing one for a position spends it,
        and which assignment is optimal is a question. Here the objective
        decomposes over positions: each one independently reports the minimum of
        its own class and nothing is spent, so the pointwise minimiser is the
        global one and there is nothing to trade off. Same phrase in the
        statement, two different objects underneath it.

        `O(|s1| * alpha + |baseStr|)` time, `O(1)` space - the union-find is 26
        cells wide regardless of the input.
        """
        dsu = SmallestRootDSU(26)
        for a, b in zip(s1, s2):
            dsu.union(ord(a) - 97, ord(b) - 97)

        # `find` already returns the smallest letter of the class, so there is no
        # root -> min table between the structure and the answer. that table is
        # what a size-balanced union rule would have forced, and building it was
        # the mistake here, same shape as the email -> account map in 721. worth
        # naming the cost though: union by smallest gives up the balancing, so
        # the trees can degenerate to a chain. on 26 elements with path
        # compression that is free. on a large universe it would not be, and
        # there the second table is the right answer rather than the sloppy one.
        return "".join(chr(97 + dsu.find(ord(c) - 97)) for c in baseStr)


if __name__ == "__main__":
    solution = Solution()
    cases = [
        ("parker", "morris", "parser", "makkek"),
        ("hello", "world", "hold", "hdld"),
        ("leetcode", "programs", "sourcecode", "aauaaaaada"),
    ]
    for s1, s2, base, expected in cases:
        got = solution.smallestEquivalentString(s1, s2, base)
        print(f"{base!r:>14} -> {got!r:<14} expected {expected!r}  {'ok' if got == expected else 'FAIL'}")
