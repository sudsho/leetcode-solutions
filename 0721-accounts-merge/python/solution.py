from collections import defaultdict
from typing import Dict, List


class DSU:
    """Disjoint sets over `0..n-1`, union by size with path compression.

    The elements here are *account indices*, not emails, and that is the one
    design decision in this file worth arguing about. See `accountsMerge`.
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
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """Merge accounts sharing any email; emit `[name, *sorted(emails)]` each.

        Same shape as the last three days - a partition, and an answer that has
        to be printed one class at a time. What is new is that the output has
        three parts and they sit in three *different* places on the quotient /
        section distinction, which is why this one is worth writing down.

        **The partition is the quotient and is the bulk of the answer.** Sharing
        an email is not itself transitive; the relation being quotiented by is
        its transitive closure, which is what the DSU computes. Nothing in the
        output depends on which shared email caused two accounts to merge, so
        the edges can be discarded once merged - the same fact as in 1202, where
        `pairs` was a presentation and only the components survived.

        **The email list is not a section at all.** A class determines a *set* of
        emails, and a set has no preferred listing, so the output has to fix one
        or two correct answers would compare unequal. But sorting is a rendering
        convention on a determined object, not a choice of representative from an
        orbit: there is no group acting, and no element is being picked out. It
        looked like the 711 hash key at first glance and it is not the same
        thing, which is the trap this problem sets.

        **The name is the interesting one.** It is one member's copy of a field,
        chosen from the class with nothing behind the choice, and unlike the 711
        key it is *printed*. By the axis from the 31st - is the choice observable
        in the answer - that should put it with 1202, where the section is the
        output and needed a real exchange argument to justify. It needs no
        argument at all. The reason is that `name` is constant on classes:
        accounts merge only through a shared email, a shared email means one
        person, and one person's accounts all carry the same name. So the pick is
        observable and still free, because what is observed does not vary across
        the thing being picked from.

        That is a refinement of the 31st rather than a counterexample to it.
        Observability is the right question; it is just not the last one. A
        choice needs justifying when the observable part varies across the class,
        and 1202 is the case where it does - permuting a component's characters
        changes the string that gets printed - while here it cannot.

        `O(sum_i |A_i| * alpha + E log E)` time for `E` distinct emails, the sort
        dominating; `O(E)` space.
        """
        dsu = DSU(len(accounts))

        # first account index to claim each email. a repeat claim is an edge.
        owner: Dict[str, int] = {}
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in owner:
                    dsu.union(i, owner[email])
                else:
                    owner[email] = i

        # keyed by email, so each email appears once and the per-class lists are
        # duplicate-free before they are sorted - no dedup step to skip.
        emails_by_root = defaultdict(list)
        for email, i in owner.items():
            emails_by_root[dsu.find(i)].append(email)

        # `accounts[root][0]` is safe for any root in the class, not just this
        # one: the name is an invariant of the class, per the docstring.
        return [
            [accounts[root][0]] + sorted(emails)
            for root, emails in emails_by_root.items()
        ]
