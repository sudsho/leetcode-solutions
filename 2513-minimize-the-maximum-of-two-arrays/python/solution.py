import random
from math import gcd


class Solution:
    def minimizeSet(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2):
        # thirteenth on the monotone-predicate-plus-bisect shape, second one
        # today, and it settles this morning's question from the other side.
        #
        # 2226 had an expression for a predicate and still had to bisect, and i
        # blamed the sum: `sum(c // t)` is written down but it is a sum over the
        # input, so it is opaque at the level that matters and its breakpoints
        # number n * sqrt(C). the conclusion was that the axis is not "expression
        # versus black box" but how many breakpoints you can locate cheaply.
        #
        # that conclusion had an escape hatch in it. every predicate that had ever
        # been O(1) in this run - one of them, 1802 - was also invertible, so
        # "cheap to evaluate" and "few breakpoints" had never been separated, and
        # 2226's predicate was O(n), which leaves the scan available as the
        # explanation.
        #
        # this predicate is O(1). three floor divisions and a comparison, no
        # dependence on anything but the four inputs. and it has a breakpoint at
        # every multiple of divisor1, of divisor2 and of their lcm below the
        # answer, which at the constraint ceiling is millions of them, so there is
        # nothing to invert and the bisect is not avoidable.
        #
        # so O(1) does not imply invertible, the scan was never the reason, and
        # this morning's replacement survives the test i could not run then.
        # 1802 is invertible because it has three pieces, and three is a fact
        # about the tent's geometry rather than about the cost of evaluating it.
        low, high = 1, 2 * (uniqueCnt1 + uniqueCnt2)

        # minimization, so the true half keeps mid and mid rounds *down*. tenth
        # minimization in thirteen, and the rule gets written out every time
        # because the two roundings are the same keystroke apart.
        while low < high:
            mid = (low + high) // 2
            if self._fits(divisor1, divisor2, uniqueCnt1, uniqueCnt2, mid):
                high = mid
            else:
                low = mid + 1

        return low

    def _fits(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2, ceiling):
        """Can `1..ceiling` supply both arrays?

        Split `[1, ceiling]` by divisibility. Writing `lcm` for the lcm of the two
        divisors:

            reserved for arr1 : divisible by divisor2 only  -> arr2 cannot take it
            reserved for arr2 : divisible by divisor1 only  -> arr1 cannot take it
            free              : divisible by neither        -> either may take it
            dead              : divisible by both           -> nobody may take it

        by inclusion-exclusion, and then feasibility is three inequalities:

            uniqueCnt1 <= reserved1 + free
            uniqueCnt2 <= reserved2 + free
            uniqueCnt1 + uniqueCnt2 <= reserved1 + reserved2 + free

        **These are Hall's condition, and that is why they are sufficient and not
        only necessary.** The bipartite graph has two demand nodes, so its subsets
        are the empty set and the three above, and Hall's theorem says a matching
        saturating the demand exists exactly when every subset's neighbourhood is
        big enough. Four subsets, one of them vacuous, three inequalities.

        That is a different situation from every previous predicate in the run.
        2141's work count proved necessity and nothing else, and sufficiency
        needed a construction with its own argument. The nine before it got both
        halves in one breath because a greedy built the witness while testing for
        it. Here neither happens: nothing is constructed, and both halves come out
        anyway, because a theorem is doing the work that a construction did on the
        21st.

        So the witness's *existence* is certified without the witness. That is the
        first time in thirteen problems, and it is what a completeness theorem
        buys - `minimizeSetAssignment` builds one, but it is building something
        already known to be there rather than supplying the proof.

        Monotone in the right direction. Each of the four counts is non-decreasing
        in `ceiling` and all three inequalities have the counts on the large side,
        so `{ceiling : fits}` is a suffix. Third distinct source of monotonicity in
        the run after the greedies and 2141's concavity, and the plainest.

        `O(1)`, and one `gcd`.
        """
        multiple = divisor1 // gcd(divisor1, divisor2) * divisor2

        dead = ceiling // multiple
        reserved1 = ceiling // divisor2 - dead
        reserved2 = ceiling // divisor1 - dead
        free = ceiling - ceiling // divisor1 - ceiling // divisor2 + dead

        # the third inequality is `ceiling - dead` on the right, since the three
        # live classes partition everything that is not dead. written the long way
        # because the long way is the one that reads as Hall's condition, and the
        # short way reads as a coincidence.
        return (
            uniqueCnt1 <= reserved1 + free
            and uniqueCnt2 <= reserved2 + free
            and uniqueCnt1 + uniqueCnt2 <= reserved1 + reserved2 + free
        )

    def minimizeSetAssignment(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2):
        """Return `(ceiling, arr1, arr2)` - the answer and two arrays realising it.

        Nineteenth day of the summary-versus-set split, and a third source of
        canonicity after the two this morning.

        The witness is canonical, and not for either of today's earlier reasons.
        2226 had a certificate set closed under join and 1802 had one closed under
        meet, with the direction set by which way the constraint's inequality
        points. Here there is no lattice on offer at all: the object is a pair of
        disjoint sets and pointwise operations on pairs of sets do not preserve
        the counts, which are equalities rather than bounds.

        What makes it canonical instead is that the candidate pool is **totally
        ordered**. Take the reserved numbers first because nothing else can use
        them, then fill both arrays from the free pool in increasing order, arr1
        before arr2. Every choice along the way is between numbers, and numbers
        come with an order, so "smallest" names a member the way "leftmost" does
        in 1898.

        Three sources now, and they are genuinely different: meet-closure,
        join-closure, and a total order on the candidates with no lattice
        anywhere. The 21st separated slack from symmetry and the 22nd added a
        lattice fact as a third thing the word can mean; this is a fourth, and the
        honest summary is that "canonical" has been a bucket rather than a
        property for nineteen days.

        Note that arr1-before-arr2 is a real choice and it is not forced - the two
        arrays are not symmetric (their constraints differ) but neither is
        distinguished by the problem, so the rule is a convention. The tests check
        the sets are valid rather than checking them against this exact output,
        which is the split the 21st introduced.

        `O(ceiling)` and therefore only usable on small inputs, which is why the
        primary does not go anywhere near it.
        """
        ceiling = self.minimizeSet(divisor1, divisor2, uniqueCnt1, uniqueCnt2)

        arr1, arr2, free = [], [], []
        for value in range(1, ceiling + 1):
            bad1 = value % divisor1 == 0
            bad2 = value % divisor2 == 0
            if bad1 and bad2:
                continue
            if bad1:
                arr2.append(value)
            elif bad2:
                arr1.append(value)
            else:
                free.append(value)

        arr1 = arr1[:uniqueCnt1]
        arr2 = arr2[:uniqueCnt2]

        cursor = 0
        while len(arr1) < uniqueCnt1:
            arr1.append(free[cursor])
            cursor += 1
        while len(arr2) < uniqueCnt2:
            arr2.append(free[cursor])
            cursor += 1

        # unreachable when the predicate is right, and that is exactly why it is
        # checked. Hall's condition says a matching exists; this loop is the only
        # thing that says this particular greedy finds one. the theorem does not
        # certify the algorithm.
        if len(arr1) != uniqueCnt1 or len(arr2) != uniqueCnt2:
            raise AssertionError("feasible ceiling did not fill both arrays")

        return ceiling, arr1, arr2

    def minimizeSetSameDivisor(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2):
        """Shortcut for `divisor1 == divisor2`: the two arrays share one pool.

        Both reserved classes are empty, so the three inequalities collapse to the
        third one and the split between the arrays stops mattering entirely - only
        the total does. Same role as 2141's `n == 1` and 2226's `k == 1`: the input
        where the algorithm makes no decision, so the general path has something
        with no choices in it to agree with.

        The answer is the least `t` with `t - t // d >= c1 + c2`. Still a search,
        but over one inequality rather than three, and it is a genuinely different
        computation rather than the same one with an argument fixed - which is
        what makes the agreement worth asserting.

        Returns `None` when it does not apply.
        """
        if divisor1 != divisor2:
            return None

        needed = uniqueCnt1 + uniqueCnt2
        low, high = 1, 2 * needed

        while low < high:
            mid = (low + high) // 2
            if mid - mid // divisor1 >= needed:
                high = mid
            else:
                low = mid + 1

        return low


if __name__ == "__main__":
    s = Solution()

    assert s.minimizeSet(2, 7, 1, 3) == 4
    assert s.minimizeSet(3, 5, 2, 1) == 3
    assert s.minimizeSet(2, 4, 8, 2) == 15

    cases = [
        (2, 7, 1, 3),
        (3, 5, 2, 1),
        (2, 4, 8, 2),
        (2, 2, 3, 3),
        (2, 3, 1, 1),
        (5, 5, 1, 1),
        (2, 3, 6, 6),
        (7, 11, 4, 9),
        (2, 100000, 5, 5),
        (100000, 100000, 1, 1),
        (4, 6, 10, 10),
        (9, 3, 7, 2),
        (2, 5, 1, 20),
        (13, 17, 30, 1),
    ]

    for d1, d2, c1, c2 in cases:
        assert d1 >= 2 and d2 >= 2, (d1, d2)
        assert c1 >= 1 and c2 >= 1, (c1, c2)

    # bounds, ninth day. the bottom end is `1` and it is *not* generally feasible,
    # same as 2226 this morning - but unlike 2226 there is no zero to fall back
    # to, because the answer is a value in the search space by definition. so the
    # bottom is a range end with no claim attached to it, which is a third kind
    # after "feasible by arithmetic" and "feasible by a promise in the statement".
    #
    # the top end is derived rather than guessed. both divisors are at least 2, so
    # at most half of [1, t] is divisible by either one of them, hence
    # `t - t // divisor >= t / 2` and `t - t // lcm >= t / 2`. all three
    # inequalities are then satisfied at `t = 2 * (c1 + c2)`. asserted rather than
    # trusted, because the whole search is inside it.
    for d1, d2, c1, c2 in cases:
        assert s._fits(d1, d2, c1, c2, 2 * (c1 + c2)), (d1, d2, c1, c2)
        assert s.minimizeSet(d1, d2, c1, c2) <= 2 * (c1 + c2)

    # and the ceiling is a bound rather than an achievable target - it is derived
    # by throwing away everything except "at least half survives", so it is only
    # tight when both divisors are 2 and they collide everywhere. fifth day
    # running that the extreme end of the range is not the answer for anything.
    loose = [c for c in cases if s.minimizeSet(*c) < 2 * (c[2] + c[3])]
    assert loose, "the top bound is attained on every case, so it is not a bound"

    # the predicate against its own definition, counted the slow obvious way. a
    # predicate that is wrong but still monotone hands back a confident wrong
    # boundary and nothing downstream notices.
    def fits_brute(d1, d2, c1, c2, t):
        reserved1 = reserved2 = free = 0
        for value in range(1, t + 1):
            bad1 = value % d1 == 0
            bad2 = value % d2 == 0
            if bad1 and bad2:
                continue
            if bad1:
                reserved2 += 1
            elif bad2:
                reserved1 += 1
            else:
                free += 1
        return (
            c1 <= reserved1 + free
            and c2 <= reserved2 + free
            and c1 + c2 <= reserved1 + reserved2 + free
        )

    for d1, d2, c1, c2 in cases:
        span = min(2 * (c1 + c2), 400)
        for t in range(1, span + 1):
            assert s._fits(d1, d2, c1, c2, t) == fits_brute(d1, d2, c1, c2, t), (
                d1,
                d2,
                c1,
                c2,
                t,
            )

    # monotonicity in the direction the bisect uses - a suffix, not a prefix,
    # because this is a minimization and the flags have to go False then True.
    for d1, d2, c1, c2 in cases:
        span = min(2 * (c1 + c2), 400)
        flags = [s._fits(d1, d2, c1, c2, t) for t in range(1, span + 1)]
        assert all(a <= b for a, b in zip(flags, flags[1:])), (d1, d2, c1, c2)

    # necessity: one below the answer fails. together with the assignment built at
    # the answer this pins it exactly, and neither half is brute force.
    for d1, d2, c1, c2 in cases:
        answer = s.minimizeSet(d1, d2, c1, c2)
        assert answer >= 1
        if answer > 1:
            assert not s._fits(d1, d2, c1, c2, answer - 1), (d1, d2, c1, c2)

    # Hall's condition is an iff, so the assignment has to exist at the answer -
    # this is the sufficiency half, checked by construction rather than assumed
    # from the theorem. a theorem about the graph is not a theorem about the
    # greedy that walks it.
    for d1, d2, c1, c2 in cases:
        if 2 * (c1 + c2) > 3000:
            continue
        ceiling, arr1, arr2 = s.minimizeSetAssignment(d1, d2, c1, c2)
        assert ceiling == s.minimizeSet(d1, d2, c1, c2)
        assert len(arr1) == c1 and len(arr2) == c2, (d1, d2, c1, c2)
        assert len(set(arr1)) == c1 and len(set(arr2)) == c2, (d1, d2, c1, c2)
        assert not (set(arr1) & set(arr2)), (d1, d2, c1, c2)
        assert all(1 <= v <= ceiling for v in arr1 + arr2), (d1, d2, c1, c2)
        assert all(v % d1 for v in arr1), (d1, d2, c1, c2)
        assert all(v % d2 for v in arr2), (d1, d2, c1, c2)
        assert max(arr1 + arr2) <= ceiling

    # the same-divisor path agrees. it shares no code with the primary's predicate
    # and solves one inequality instead of three, so agreement is a real
    # cross-check and not a restatement.
    for d1, _, c1, c2 in cases:
        assert s.minimizeSetSameDivisor(d1, d1, c1, c2) == s.minimizeSet(
            d1, d1, c1, c2
        ), (d1, c1, c2)

    assert s.minimizeSetSameDivisor(2, 3, 1, 1) is None

    # swapping the two arrays swaps the two divisors and nothing else, so the
    # answer is invariant under doing both. this is a symmetry of the problem and
    # not of the implementation, and _fits treats the two sides asymmetrically
    # enough - reserved1 comes off divisor2 - that an index slip would survive
    # every check above and die here.
    for d1, d2, c1, c2 in cases:
        assert s.minimizeSet(d1, d2, c1, c2) == s.minimizeSet(d2, d1, c2, c1), (
            d1,
            d2,
            c1,
            c2,
        )

    # random cases against a sweep, which is the only check that does not go
    # through the bisect at all.
    rng = random.Random(2513)
    for _ in range(400):
        d1 = rng.randint(2, 12)
        d2 = rng.randint(2, 12)
        c1 = rng.randint(1, 25)
        c2 = rng.randint(1, 25)

        answer = s.minimizeSet(d1, d2, c1, c2)

        sweep = None
        for t in range(1, 2 * (c1 + c2) + 1):
            if fits_brute(d1, d2, c1, c2, t):
                sweep = t
                break
        assert sweep == answer, (d1, d2, c1, c2, sweep, answer)

        _, arr1, arr2 = s.minimizeSetAssignment(d1, d2, c1, c2)
        assert len(set(arr1) | set(arr2)) == c1 + c2, (d1, d2, c1, c2)

    # and at the constraint ceiling, because the whole note today is about how
    # many breakpoints the predicate has and every case above is small enough to
    # have almost none.
    for d1, d2, c1, c2 in ((2, 3, 10 ** 9, 10 ** 9), (99991, 99989, 10 ** 9, 1)):
        answer = s.minimizeSet(d1, d2, c1, c2)
        assert s._fits(d1, d2, c1, c2, answer)
        assert not s._fits(d1, d2, c1, c2, answer - 1)

    print("all good")
