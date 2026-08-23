import random


class Solution:
    def maximumCandies(self, candies, k):
        # twelfth on the monotone-predicate-plus-bisect shape, and the first test
        # of the axis i named yesterday.
        #
        # yesterday's claim was that the ten days before 1802 all bisected because
        # their predicates were black boxes - things you could only *call* - and
        # that 1802 was different because its predicate was an expression, so it
        # could be inverted instead of searched. the axis was black box versus
        # expression, and i said that one was a property of the problem rather
        # than of the constraint block.
        #
        # this predicate is an expression. `sum(c // t) >= k`, written down, no
        # greedy inside it, nothing to simulate. and it is not invertible, and no
        # amount of staring at it makes it invertible, because a sum of n floors
        # is a step function with n * sqrt(C) breakpoints and no closed form for
        # the place it crosses a level.
        #
        # so the axis was too coarse by exactly one notch. 1802 inverted because
        # its predicate was an expression *in one piece* - three polynomial pieces
        # with known breakpoints, each one solvable. an expression built out of a
        # sum over the input is still opaque at the level that matters. what
        # separates the two is not whether you can write the predicate down; it is
        # whether its breakpoints are few enough to enumerate. which is the size
        # question again, and i had thought i was replacing the size question.
        if k <= 0:
            return 0

        total = sum(candies)

        # bounds, eighth day, and the bottom end is a new kind.
        #
        # the previous eleven all had a bottom that was either trivially feasible
        # by arithmetic or promised feasible by the statement. here the bottom of
        # the search space is `t = 1`, and `sum(c // 1) = total`, so it is feasible
        # exactly when `total >= k` and infeasible otherwise.
        #
        # `t = 0` is not the answer to that. it is not in the search space at all -
        # the predicate does not extend there, because `c // 0` is not a number.
        # so the zero this returns is a value the problem defines outside the
        # search rather than a point the search reaches, and the guard is forced
        # by the arithmetic of the predicate rather than by a convention about
        # what to report. 1482 returned -1 from a predicate that was perfectly
        # well defined at the impossible point and merely false there; this is the
        # first time the predicate has a domain that stops.
        if total < k:
            return 0

        # top: k children at t candies each need k * t candies and there are only
        # `total`, so t <= total // k. and this one is genuinely a bound rather
        # than an achievable configuration - [1, 1, 5], k = 3 has total // k = 2
        # and an answer of 1, because the two singleton piles cannot be merged to
        # make a second pile of 2. fourth day running that the ceiling is not
        # attained, and the reason is the same shape as 2141's stranded battery:
        # a resource that exists and cannot be delivered where it is needed.
        low, high = 1, total // k

        # maximization, so the true half keeps mid and mid rounds up.
        while low < high:
            mid = (low + high + 1) // 2
            if self._enough_piles(candies, mid, k):
                low = mid
            else:
                high = mid - 1

        return low

    def _enough_piles(self, candies, size, k):
        """Can `candies` be cut into at least `k` sub-piles of exactly `size`?

        `sum(c // size) >= k`. Pile `c` yields `c // size` whole sub-piles of that
        size and the remainder is unusable, because piles may be divided and may
        not be merged - so the floor is not an approximation, it is the rule.

        Monotone in the right direction, and the argument is the plain one for
        once. `c // t` is non-increasing in `t` for each `c`, a sum of
        non-increasing functions is non-increasing, so `{t : sum >= k}` is a
        prefix. No greedy to read it off (the previous nine), no concavity
        (2141), no least element (1802) - just a sum of monotone terms.

        Worth saying that this is the first predicate in the run where
        monotonicity is *obvious* and the interesting structure is somewhere else
        entirely. Eleven days of the monotonicity being the thing that needed an
        argument had me reading it as where the content lives. It isn't; it is
        just the admission ticket.

        `O(len(candies))` and no allocation.
        """
        piles = 0

        for pile in candies:
            piles += pile // size
            if piles >= k:
                return True

        return piles >= k

    def maximumCandiesByCandidates(self, candies, k):
        """Same answer, searched over the values the answer can actually take.

        **The answer is always `c // q` for some pile `c` and some positive `q`.**
        Let `t` be the answer, so `t` is feasible and `t + 1` is not. Something has
        to break between them, so some pile has `c // t > c // (t + 1)`. Write
        `q = c // t`. Then `q * t <= c` from the left half and `c < q * (t + 1)`
        from the right, so `t <= c / q < t + 1`, so `c // q = t` exactly.

        That is attainment, and it is the cleanest one in the run - the previous
        proofs went through an exchange argument on a greedy, and this is two
        inequalities and a division.

        **And the answer set is bigger than the input for the first time.** Its
        size is the number of distinct values of `c // q`, which is `O(sqrt(c))`
        per pile and so `O(n sqrt(C))` overall - with `n` at `1e5` and `C` at
        `1e7`, several million. On the 21st I concluded that `|answer set|` is
        always at least `n` while `log(range)` is capped by the width of a machine
        integer, so the comparison is decided by the venue. Three days later here
        is a problem where the answer set is *superlinear* in the input, and the
        gap is wider still: 24 predicate calls against a candidate set i cannot
        afford to build.

        The lopsidedness has now been confirmed by a case whose candidate
        structure is completely unlike the previous eleven. Those were all one
        candidate per input element - a gap, a ratio, a value. This one is a
        divisor lattice, and it is the first time the answer set's size has not
        been `n` on the nose. It got bigger. It has never once got smaller.

        Kept because agreement with the primary is a real test of the attainment
        proof above, and that proof is the one new mathematical thing today.

        `O(n sqrt(C))` to build, `O(log)` to search. Unusable at the constraint
        ceiling and fine on the test cases.
        """
        if k <= 0:
            return 0

        total = sum(candies)
        if total < k:
            return 0

        sizes = self._candidate_sizes(candies, total // k)

        low, high = 0, len(sizes) - 1
        while low < high:
            mid = (low + high + 1) // 2
            if self._enough_piles(candies, sizes[mid], k):
                low = mid
            else:
                high = mid - 1

        return sizes[low]

    def _candidate_sizes(self, candies, ceiling):
        """Every distinct `c // q` across the piles, capped at `ceiling`, sorted.

        Divisor-block enumeration: `c // q` is constant on runs of `q`, and the
        run containing `q` ends at `c // (c // q)`. So jump run to run rather than
        stepping, which is what makes this `O(sqrt(c))` per pile instead of
        `O(c)`.

        Always contains 1 when the piles are positive, since `c // c == 1`, so the
        bisect below has a floor to land on and the caller has already ruled out
        the empty case.
        """
        values = set()

        for pile in candies:
            q = 1
            while q <= pile:
                value = pile // q
                if value <= ceiling:
                    values.add(value)
                q = pile // value + 1

        return sorted(values)

    def maximumCandiesCertificate(self, candies, k):
        """Return `(size, take)` - the answer and how many sub-piles each pile gives.

        Eighteenth day of the summary-versus-set split, and the first time the two
        witnesses in the room disagree about whether they are canonical.

        There are two different objects here and eleven days of them coinciding
        had me treating them as one. The **certificate** is the thing that proves
        `t` feasible: a vector `v` with `v_i <= c_i // t` and `sum(v) >= k`. The
        **allocation** is the thing the problem asks for: an assignment of exactly
        `k` sub-piles to `k` named children. Yesterday those were the same object -
        the tent was simultaneously what proved the sum bound and what you would
        hand in - and on the 21st they came apart for the first time, where the
        work count proved feasibility and the schedule had to be built separately.

        Today they come apart again and the canonicity lands on the other one.

        The certificate set is closed under pointwise **maximum**: if `v` and `w`
        both satisfy the constraints then so does `max(v, w)`, because the upper
        bounds are per-coordinate and the sum only goes up. A nonempty set of
        integer vectors closed under join and bounded above has a **greatest**
        element, and it is `v_i = c_i // t` - take everything. So the certificate
        is canonical, by exactly yesterday's argument run upside down.

        That the dual works is not an accident of the two problems. Yesterday's
        constraint was an upper bound on a sum, so shrinking was safe and the meet
        survived; today's is a lower bound on a sum, so growing is safe and the
        join survives. **The direction of the lattice is set by the direction of
        the constraint**, and 1802 read as a fact about that problem when it is a
        fact about which way the inequality points.

        The allocation is not canonical and cannot be made so. Children are
        interchangeable by definition, which is 2141's `n!` relabelings verbatim,
        and on top of that the certificate usually has slack - `sum(c_i // t)`
        exceeds `k` - so there is a choice of *which* sub-piles go unused before
        there is any question of who gets what.

        So the honest statement is that this problem has a canonical witness and
        an uncanonical one, and which you get depends on which question you asked.
        The tests below split accordingly: equality against the greatest element
        for the certificate, property check for the allocation.

        `O(n)` after the primary.
        """
        size = self.maximumCandies(candies, k)
        if size == 0:
            return 0, []

        take = [pile // size for pile in candies]

        # unreachable when the predicate is right, and that is why it is checked.
        # the primary says t is feasible; this line is the only thing that says
        # the certificate it implies actually has k sub-piles in it.
        if sum(take) < k:
            raise AssertionError("feasible size did not yield k sub-piles")

        return size, take

    def maximumCandiesAllocation(self, candies, k):
        """Return `(size, plan)` with `plan` a list of `(pile, count)` summing to `k`.

        The leftmost member of the uncanonical set: walk the piles in index order
        and take from each until `k` sub-piles are accounted for. Pile indices are
        not symmetric, so leftmost names a member the way it does in 1898 - but
        only in the space where piles carry their index. Two piles of equal size
        are interchangeable, so in the quotient by pile *value* this choice
        evaporates, which is 2616's point and the reason the test on this one is a
        property check.
        """
        size = self.maximumCandies(candies, k)
        if size == 0:
            return 0, []

        plan = []
        remaining = k

        for index, pile in enumerate(candies):
            if remaining == 0:
                break
            count = pile // size
            if count > remaining:
                count = remaining
            if count:
                plan.append((index, count))
                remaining -= count

        if remaining:
            raise AssertionError("allocation ran out of piles before k")

        return size, plan

    def maximumCandiesSingle(self, candies, k):
        """Shortcut for `k == 1`: the answer is the largest pile.

        One child, so no splitting between piles is ever needed and the whole
        problem is a max. Same role as 2141's `n == 1` and 2517's `k == 2` - the
        input where the algorithm makes no decision, which makes it the cleanest
        thing to check the general path against. It is also the input that pushes
        the search range to its ceiling, which random cases essentially never do.

        Returns `None` when it does not apply.
        """
        if k != 1:
            return None

        return max(candies)


if __name__ == "__main__":
    s = Solution()

    assert s.maximumCandies([5, 8, 6], 3) == 5
    assert s.maximumCandies([2, 5], 11) == 0
    assert s.maximumCandies([1, 2, 3, 4, 10], 5) == 3
    assert s.maximumCandies([4, 7, 5], 4) == 3
    assert s.maximumCandies([1, 1, 1], 3) == 1

    cases = [
        ([5, 8, 6], 3),
        ([2, 5], 11),
        ([1, 2, 3, 4, 10], 5),
        ([4, 7, 5], 4),
        ([1, 1, 1], 3),
        ([1, 1, 5], 3),
        ([100], 1),
        ([100], 100),
        ([100], 101),
        ([9, 9, 9], 1),
        ([1, 2, 3], 6),
        ([1, 2, 3], 7),
        ([10, 10, 10, 10], 5),
        ([7], 3),
        ([1000000000], 1),
        ([2, 2, 2, 2, 2], 5),
        ([6, 6, 6], 4),
        ([3, 5, 7, 11], 6),
    ]

    for candies, k in cases:
        assert all(c >= 1 for c in candies), candies
        assert k >= 1, k

    # the ends of the range, checked rather than asserted in prose. eighth day of
    # writing a bounds paragraph and the fourth of turning it into asserts.
    #
    # the bottom end is the new one today and it splits by feasibility, which no
    # previous day's bottom did. when total >= k the size 1 is feasible by
    # arithmetic; when it is not, the answer is 0 and the search never runs. both
    # branches get stated, because the interesting claim is that there is no third
    # case - in particular there is no input where the search runs and returns
    # something the predicate rejects.
    for candies, k in cases:
        total = sum(candies)
        if total >= k:
            assert s._enough_piles(candies, 1, k), (candies, k)
            assert s.maximumCandies(candies, k) >= 1, (candies, k)
        else:
            assert not s._enough_piles(candies, 1, k), (candies, k)
            assert s.maximumCandies(candies, k) == 0, (candies, k)

    # the top end is a bound and nothing attains it in general, so it is tested as
    # a bound - the point above it fails - and not as a point.
    for candies, k in cases:
        if sum(candies) < k:
            continue
        ceiling = sum(candies) // k
        assert s.maximumCandies(candies, k) <= ceiling, (candies, k)
        assert not s._enough_piles(candies, ceiling + 1, k), (candies, k)

    # the predicate against its own definition, computed the slow obvious way. a
    # predicate that is wrong but still monotone hands back a confident wrong
    # boundary and nothing downstream notices.
    def enough_brute(candies, size, k):
        return sum(c // size for c in candies) >= k

    def thresholds(candies, k):
        span = sum(candies) // max(k, 1) + 3
        window = set(range(1, min(300, span + 1)))
        window |= set(range(max(1, span - 300), span + 1))
        answer = s.maximumCandies(candies, k)
        if answer:
            window |= set(range(max(1, answer - 300), min(span, answer + 300) + 1))
        return sorted(window)

    for candies, k in cases:
        for size in thresholds(candies, k):
            assert s._enough_piles(candies, size, k) == enough_brute(
                candies, size, k
            ), (candies, k, size)

    # monotonicity in the direction the bisect uses. obvious today, which is
    # exactly why it gets checked - the eleven days where it needed an argument
    # were the days i actually looked at it.
    for candies, k in cases:
        flags = [s._enough_piles(candies, size, k) for size in thresholds(candies, k)]
        assert all(a >= b for a, b in zip(flags, flags[1:])), (candies, k)

    # necessity: one above the answer fails the predicate, and the predicate is
    # exact rather than a relaxation, so nothing larger is possible.
    for candies, k in cases:
        answer = s.maximumCandies(candies, k)
        if answer:
            assert not enough_brute(candies, answer + 1, k), (candies, k)

    # attainment stated directly - the answer really is c // q for some pile and
    # some q. this is today's one new proof and the agreement check below would
    # survive both implementations being wrong the same way.
    for candies, k in cases:
        answer = s.maximumCandies(candies, k)
        if not answer:
            continue
        # `{c // q : q >= 1}` is exactly `{v : v == c // (c // v)}`, so membership
        # is one division rather than a sweep over q. worth having as its own
        # line: the sweep is what i wrote first and on [1000000000] it is a
        # billion iterations to check a fact that costs two.
        assert any(
            answer <= c and c // (c // answer) == answer for c in candies
        ), (candies, k, answer)

    # the candidate-space search agrees, which tests attainment from the other
    # side: if the answer were ever outside the divisor-floor set this would
    # return something smaller.
    for candies, k in cases:
        assert s.maximumCandiesByCandidates(candies, k) == s.maximumCandies(
            candies, k
        ), (candies, k)

    # the certificate is the greatest element, checked as an equality because
    # today's claim is that this witness is canonical. anything less than
    # take-everything is still a certificate, so a property check would pass on a
    # non-canonical answer and prove nothing.
    for candies, k in cases:
        size, take = s.maximumCandiesCertificate(candies, k)
        if size == 0:
            assert take == []
            continue
        assert take == [c // size for c in candies], (candies, k)
        assert sum(take) >= k, (candies, k)
        # closed under join, which is the reason the greatest element exists.
        # any certificate joined with this one is this one.
        for scale in (1, 2, 3):
            other = [max(0, t - scale) for t in take]
            if sum(other) >= k:
                assert [max(a, b) for a, b in zip(other, take)] == take

    # the allocation is a property check, because it is the uncanonical witness.
    # exactly k sub-piles, none drawn from a pile that cannot supply it, and no
    # pile over-drawn.
    for candies, k in cases:
        size, plan = s.maximumCandiesAllocation(candies, k)
        if size == 0:
            assert plan == []
            continue
        assert sum(count for _, count in plan) == k, (candies, k)
        seen = set()
        for index, count in plan:
            assert index not in seen, (candies, k, index)
            seen.add(index)
            assert 1 <= count <= candies[index] // size, (candies, k, index, count)

    # k == 1 removes the splitting decision and therefore the problem, so the
    # general path has to agree with the max.
    for candies, _ in cases:
        assert s.maximumCandies(candies, 1) == s.maximumCandiesSingle(candies, 1), candies

    assert s.maximumCandiesSingle([1, 2], 2) is None

    # every k from 1 up past the total on the same array, so the boundary between
    # "answer exists" and "answer is zero" is walked across rather than sampled.
    # more children can never get more each, which is monotonicity of the problem
    # in k rather than of the predicate in t - a different claim, and nothing else
    # here would catch it failing.
    for candies, _ in cases:
        total = sum(candies)
        if total <= 400:
            ks = list(range(1, total + 3))
        else:
            # subsampled, and the monotonicity claim survives subsampling because
            # a non-increasing sequence restricted to any subsequence is still
            # non-increasing. the two ends are kept exactly, since the crossing
            # from "answer exists" to "answer is zero" happens at total and that
            # is the only place worth walking across.
            ks = sorted(
                set(range(1, 50)) | {total - 1, total, total + 1, total + 2}
            )
        previous = None
        for k in ks:
            answer = s.maximumCandies(candies, k)
            if previous is not None:
                assert answer <= previous, (candies, k, answer, previous)
            previous = answer
        assert previous == 0, candies

    # the input where the ceiling is unreachable because a resource exists and
    # cannot be delivered. asserted directly because the property checks above
    # would all pass on an implementation that quietly allowed merging piles.
    assert s.maximumCandies([1, 1, 5], 3) == 1
    assert sum([1, 1, 5]) // 3 == 2

    # random cases across all three implementations. the fixed cases are all
    # hand-picked for a reason and hand-picked cases stop finding things once they
    # pass once.
    rng = random.Random(2226)
    for _ in range(600):
        n = rng.randint(1, 8)
        candies = [rng.randint(1, 40) for _ in range(n)]
        k = rng.randint(1, sum(candies) + 2)

        answer = s.maximumCandies(candies, k)
        assert s.maximumCandiesByCandidates(candies, k) == answer, (candies, k)

        # against a sweep, which is the only check here that does not go through
        # the bisect at all.
        sweep = 0
        for size in range(1, sum(candies) + 1):
            if enough_brute(candies, size, k):
                sweep = size
        assert sweep == answer, (candies, k, sweep, answer)

        if answer:
            _, plan = s.maximumCandiesAllocation(candies, k)
            assert sum(count for _, count in plan) == k, (candies, k)

    # and a large one, because every case above is small enough that the candidate
    # set and the range cost the same, and the whole argument in today's note is
    # about what happens when they do not.
    big = [rng.randint(1, 10 ** 7) for _ in range(3000)]
    for k in (1, 2, 1000, 10 ** 6):
        answer = s.maximumCandies(big, k)
        assert answer >= 0
        if answer:
            assert s._enough_piles(big, answer, k)
            assert not s._enough_piles(big, answer + 1, k)

    print("all good")
