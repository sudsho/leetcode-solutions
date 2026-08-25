import random
from math import gcd

MOD = 10 ** 9 + 7


class Solution:
    def nthMagicalNumber(self, n, a, b):
        # fifteenth on the monotone-predicate-plus-bisect shape, and the second
        # in a row where the bisect does not happen. yesterday that was the
        # headline. today it is the setup.
        #
        # yesterday's rule, written down after three days of arguing about what
        # makes a predicate invertible, was that two things are needed: the
        # predicate has to be a **conjunction** rather than an aggregate, and the
        # individual terms have to be solvable. 2226 failed the first, 2513 the
        # second, and 1802 and 2439 passed both.
        #
        # the predicate here is
        #
        #     count(t)  =  t//a + t//b - t//L  >=  n            (L = lcm(a, b))
        #
        # which is an aggregate. not "an aggregate in spirit" - it is a sum of
        # floor terms with the terms coupled by the summation, structurally the
        # same object as 2226's sum(c//t) >= k, down to the floors. by yesterday's
        # rule it does not invert.
        #
        # it inverts. exactly, in O(a + b), with no search at all.
        #
        # the reason has nothing to do with decomposing the sum, because the sum
        # does not decompose. it is that `a | L` and `b | L`, so
        #
        #     count(t + L)  =  count(t) + (L//a + L//b - 1)  =  count(t) + P
        #
        # for **every** t. the predicate is not separable, it is *equivariant* -
        # it commutes with translation by L up to a constant - and that is enough
        # on its own. write n = qP + r, and the answer is q periods plus the
        # position of r inside one of them, where one period holds P magical
        # numbers and P <= a + b regardless of how large n is.
        #
        # so yesterday's rule is wrong, and this is the fourth candidate axis in
        # four days to be wrong within a day of being written down:
        #
        #   22nd  expression vs black box       killed by 2226 on the 23rd
        #   23rd  count of locatable breakpoints  killed by 2513 same night
        #   24th  conjunction, terms solvable     killed by 0878 today
        #
        # four days of looking for *the* axis, and the pattern in the failures is
        # that each candidate was one **handle** promoted to a general condition.
        # what the run has actually accumulated is a list, and the entries have
        # nothing in common with each other:
        #
        #   - algebraic separability          1802, 2439
        #   - an exchange argument shrinking the answer set   2616, 2517
        #   - local decidability of membership 2141
        #   - a symmetry of the predicate      0878, today
        #
        # bisection is what you do with a predicate offering exactly one handle,
        # evaluation at a point. anything else it offers is a shortcut, and the
        # shortcuts are unrelated. "invertible" was never a property of a
        # predicate. it was a name for "some handle exists", and naming the
        # disjunction of an open list is why every version of it died in a day.
        return self._exact(n, a, b) % MOD

    def _exact(self, n, a, b):
        """The answer as an integer, before the modulus.

        Kept separate because every claim in the test block is about the ordering
        of the magical numbers and the modulus destroys that ordering. Asserting
        `count(answer) >= n` against a value that has been reduced mod 1e9+7 is
        asserting nothing, and `n` reaches 1e9 with `a` reaching 4e4, so the true
        answer runs to about 4e13 and the reduction is not cosmetic.
        """
        lcm = a // gcd(a, b) * b
        period = lcm // a + lcm // b - 1

        full, rest = divmod(n, period)

        if rest == 0:
            # the P-th magical number in a period is the period boundary itself,
            # since L is a multiple of both. this is the branch that is easy to
            # get wrong by one period - `divmod` puts the exact multiples at
            # `rest == 0` with `full` already counting them, so the answer is
            # `full * L` and not `(full + 1) * L`.
            return full * lcm

        return full * lcm + self._within_period(rest, a, b)

    def _within_period(self, k, a, b):
        """The `k`-th smallest magical number in `(0, L]`, for `1 <= k <= P`.

        A two-pointer merge of the multiples of `a` and the multiples of `b`,
        skipping the common ones so each value is counted once. There are
        `L//a + L//b - 1` of them, and

            L//a = b // gcd(a, b)        L//b = a // gcd(a, b)

        so the merge is `O(a + b)` in the *values* of the inputs and not in
        anything that scales with `n`. That is the whole reason this is cheap:
        the search space is unbounded above and the quotient by the translation
        is finite and small.
        """
        multiple_a = a
        multiple_b = b

        for _ in range(k - 1):
            if multiple_a < multiple_b:
                multiple_a += a
            elif multiple_b < multiple_a:
                multiple_b += b
            else:
                # a common multiple: one value, two certificates. advancing both
                # pointers is the inclusion-exclusion of `- t//L` done by the
                # merge instead of by arithmetic, and forgetting it here is the
                # same bug as forgetting the third term there.
                multiple_a += a
                multiple_b += b

        return min(multiple_a, multiple_b)

    def _count(self, t, a, b):
        """`count(t)` - how many magical numbers are in `[1, t]`.

        Inclusion-exclusion, and it is worth being precise about what is being
        excluded, because it is the twenty-first day of the summary-versus-set
        split and this is a new entry in it.

        A certificate that `t` is magical is a divisor witness: a pair `(a, t//a)`
        or `(b, t//b)`. For a `t` divisible by both there are **two certificates
        for one object**, and `t//a + t//b` counts certificates rather than
        objects. Every previous day in this thread had multiplicity resolved by
        *choosing* - a leftmost convention (1898), a meet (1802), a join (2226 and
        2439), a total order on the pool (2513). Here nothing is chosen. The
        duplicates are counted and then subtracted, which works because their
        number is itself a count of the same shape, `t//L`.

        First time the witness multiplicity is corrected arithmetically rather
        than broken by a rule, and it is available only because the double-covered
        set is as easy to count as the covers are.
        """
        lcm = a // gcd(a, b) * b
        return t // a + t // b - t // lcm

    def nthMagicalNumberBisect(self, n, a, b):
        """The search this problem does not need, kept as an independent answer.

        `count` is non-decreasing, so `{t : count(t) >= n}` is a suffix and the
        minimisation keeps `mid` on the true side rounding down. Twelfth
        minimisation in fifteen.

        Bounds, eleventh day, and unlike yesterday there is a range to state.
        The bottom is `min(a, b)`, which is the first magical number and so a
        bound that is attained at `n = 1`. The top is `n * min(a, b)`: the first
        `n` multiples of the smaller are `n` distinct magical numbers, so the
        `n`-th magical number is at most the `n`-th of those. That is a bound
        with nothing attaining it in general - `n = 3, a = 2, b = 3` gives a
        ceiling of 6 and an answer of 4 - which is the fourth day running for
        that and no longer surprising.

        What is new is the width. Ten days of a range built out of the input's
        numbers, so `log(range)` was capped by the width of a machine integer -
        that was the 21st's conclusion and the reason the range side of the
        comparison could never lose by an exponent. Here the range is
        `n * min(a, b)`, up to about `4e13`, and its log is still about 45. The
        conclusion survives, which I did not expect from a problem whose search
        space is genuinely unbounded above: `n` is an *input* even though it is
        not an input length, so it is a machine integer too, and the argument
        never needed the range to be built from array entries.

        Returns the exact integer, not the residue, for the same reason `_exact`
        does.
        """
        low, high = min(a, b), n * min(a, b)

        while low < high:
            mid = (low + high) // 2
            if self._count(mid, a, b) >= n:
                high = mid
            else:
                low = mid + 1

        return low

    def nthMagicalNumberWitness(self, n, a, b):
        """Return `(answer, certificates)` - the value and every way it is magical.

        `certificates` is a sorted tuple of the divisors among `{a, b}` that
        divide the answer, so it is `(a,)`, `(b,)` or `(a, b)` with `a <= b`.
        Length two is exactly the case `_count` has to correct for, and exposing
        it makes the correction testable rather than argued: the number of `t` in
        `[1, T]` with a two-element certificate has to equal `T // lcm`, and the
        test block checks that directly instead of trusting the formula.

        `O(a + b)`.
        """
        answer = self._exact(n, a, b)

        certificates = []
        for divisor in sorted({a, b}):
            if answer % divisor == 0:
                certificates.append(divisor)

        return answer, tuple(certificates)

    def nthMagicalNumberDivides(self, n, a, b):
        """Shortcut for `a | b` or `b | a`: the answer is `n * min(a, b)`.

        If the smaller divides the larger then every multiple of the larger is
        already a multiple of the smaller, the magical numbers are exactly the
        multiples of `min(a, b)`, and the `n`-th is `n * min(a, b)` with nothing
        to merge. Equivalently `L = max(a, b)` and `P = L // min(a, b)`, so the
        period arithmetic degenerates to a single multiplication.

        Same role as 2439's non-decreasing path and 2513's equal-divisors path:
        an input where the general method makes no decisions, computed by a route
        sharing no arithmetic with it, so agreement is a cross-check rather than
        a restatement. This one is stronger than those two because it is also the
        case where the upper bound in `nthMagicalNumberBisect` is tight, so it
        pins the bound and the answer against each other at the same time.

        Returns `None` when it does not apply.
        """
        low, high = min(a, b), max(a, b)
        if high % low != 0:
            return None

        return n * low


def magical_bruteforce(limit, a, b):
    """Every magical number in `[1, limit]`, by testing each integer.

    Exponentially slower than it needs to be and that is the point - it mentions
    neither the lcm nor the period, so it is the only thing here that would still
    be right if the equivariance argument were wrong.
    """
    return [t for t in range(1, limit + 1) if t % a == 0 or t % b == 0]


if __name__ == "__main__":
    s = Solution()

    assert s.nthMagicalNumber(1, 2, 3) == 2
    assert s.nthMagicalNumber(4, 2, 3) == 6
    assert s.nthMagicalNumber(5, 2, 4) == 10
    assert s.nthMagicalNumber(3, 6, 4) == 8

    pairs = [
        (2, 3),
        (2, 4),
        (6, 4),
        (3, 3),
        (2, 2),
        (5, 7),
        (4, 6),
        (12, 18),
        (2, 40000),
        (40000, 39999),
        (9, 3),
        (35, 14),
    ]

    # the equivariance the whole file rests on. this is the one claim that turns
    # an unbounded search into an O(a + b) merge, and every other claim below is
    # downstream of it, so it gets checked against `_count` at points chosen to
    # straddle the period boundary rather than only in the middle of a period.
    for a, b in pairs:
        lcm = a // gcd(a, b) * b
        period = lcm // a + lcm // b - 1

        for t in list(range(0, min(lcm, 60))) + [lcm - 1, lcm, lcm + 1, 3 * lcm - 1]:
            assert s._count(t + lcm, a, b) == s._count(t, a, b) + period, (a, b, t)

        assert s._count(lcm, a, b) == period, (a, b)

    # `_count` against an actual enumeration, since it is inclusion-exclusion and
    # the third term is the kind of thing that is right on every example somebody
    # picks by hand and wrong on the ones where the two divisors interact.
    for a, b in pairs:
        limit = min(4 * (a // gcd(a, b) * b), 3000)
        listing = magical_bruteforce(limit, a, b)
        for t in range(0, limit + 1):
            expected = sum(1 for value in listing if value <= t)
            assert s._count(t, a, b) == expected, (a, b, t)

    # the closed form against brute force. no lcm, no period, no formula - just
    # the sorted list of integers divisible by one of them.
    for a, b in pairs:
        limit = min(6 * (a // gcd(a, b) * b), 4000)
        listing = magical_bruteforce(limit, a, b)
        for k in range(1, len(listing) + 1):
            assert s._exact(k, a, b) == listing[k - 1], (a, b, k)

    # the bisect agrees with the closed form. genuinely different computation - it
    # evaluates `count` at points it chooses and solves nothing - so agreement is
    # a cross-check on the period arithmetic, which is the one step today that
    # could be silently wrong by exactly one period.
    for a, b in pairs:
        for k in [1, 2, 3, 7, 50, 999, 100000]:
            assert s.nthMagicalNumberBisect(k, a, b) == s._exact(k, a, b), (a, b, k)

    # the `rest == 0` branch, on purpose and by construction rather than by hoping
    # a random `n` lands there. the answer at `n = m * P` has to be exactly `m`
    # periods, and the one before it has to be strictly inside the last period.
    for a, b in pairs:
        lcm = a // gcd(a, b) * b
        period = lcm // a + lcm // b - 1

        for m in (1, 2, 5, 137):
            assert s._exact(m * period, a, b) == m * lcm, (a, b, m)
            if period > 1 and m * period - 1 >= 1:
                # `period == 1` is the degenerate case `a == b`, where the only
                # magical number in a period is the boundary itself and there is
                # no strict interior to land in. it is a real input - the
                # constraints permit it - and the guard is here rather than in
                # `pairs` because the case belongs in every other check.
                previous = s._exact(m * period - 1, a, b)
                assert (m - 1) * lcm < previous < m * lcm, (a, b, m)

    # necessity and sufficiency at the boundary, which pins the answer without a
    # search and without the enumeration. neither half is brute force and neither
    # half mentions the period.
    for a, b in pairs:
        for k in [1, 4, 61, 5000, 1234567]:
            answer = s._exact(k, a, b)
            assert s._count(answer, a, b) >= k, (a, b, k)
            assert s._count(answer - 1, a, b) < k, (a, b, k)

    # the witness, and the count of double certificates. `_count` subtracts
    # `T // lcm` on the argument that that is how many values have two divisor
    # witnesses; here that number is produced by looking at each value instead.
    for a, b in pairs:
        lcm = a // gcd(a, b) * b
        limit = min(5 * lcm, 3000)

        both = sum(
            1
            for t in range(1, limit + 1)
            if t % a == 0 and t % b == 0
        )
        assert both == limit // lcm, (a, b)

        for k in (1, 2, 9, 300):
            answer, certificates = s.nthMagicalNumberWitness(k, a, b)
            assert certificates, (a, b, k)
            assert all(answer % divisor == 0 for divisor in certificates), (a, b, k)
            assert set(certificates) <= {a, b}, (a, b, k)

    # monotonicity in the direction a bisect would need, checked even though the
    # primary does not bisect. a predicate that is wrong but monotone gives a
    # confident wrong boundary and nothing downstream notices.
    for a, b in pairs:
        counts = [s._count(t, a, b) for t in range(0, 400)]
        assert all(x <= y for x, y in zip(counts, counts[1:])), (a, b)

    # the divides-shortcut, on the pairs where it applies. it shares no arithmetic
    # with the primary - one multiplication against a merge - so its agreement
    # says the merge is walking the right set and not merely walking it correctly.
    for a, b in pairs:
        for k in (1, 6, 91, 40000):
            shortcut = s.nthMagicalNumberDivides(k, a, b)
            if shortcut is not None:
                assert shortcut == s._exact(k, a, b), (a, b, k)

    assert s.nthMagicalNumberDivides(5, 6, 4) is None
    assert s.nthMagicalNumberDivides(5, 2, 6) == 10

    # random small cases against brute force, which is the only route here that
    # never mentions a period. small limits on purpose since it tests every
    # integer.
    rng = random.Random(878)
    for _ in range(400):
        a = rng.randint(2, 30)
        b = rng.randint(2, 30)

        listing = magical_bruteforce(2000, a, b)
        for _ in range(6):
            k = rng.randint(1, len(listing))
            assert s._exact(k, a, b) == listing[k - 1], (a, b, k)

    # at the constraint ceiling. `n = 1e9` with `(2, 3)` has `P = 4`, so `n` is a
    # multiple of the period and the answer is 1.5e9 exactly on a period boundary
    # - the `rest == 0` branch at full size, which is where an off-by-one-period
    # would be worth the most and show the least.
    assert s._exact(10 ** 9, 2, 3) == 1500000000
    assert s.nthMagicalNumber(10 ** 9, 2, 3) == 1500000000 % MOD

    # and at the other corner, where the answer is 2e13 - past 2**31, past 2**43,
    # and nowhere near a problem in python. this is also why the modulus is
    # applied only at the very end: reducing `full * lcm` before adding the
    # offset would be arithmetic on a residue, and the offset is not a residue.

    big = s._exact(10 ** 9, 39999, 40000)
    assert s._count(big, 39999, 40000) >= 10 ** 9
    assert s._count(big - 1, 39999, 40000) < 10 ** 9
    assert s.nthMagicalNumber(10 ** 9, 39999, 40000) == big % MOD

    # and the residue is a residue of the right thing, checked against the bisect
    # rather than against the closed form it is computed from.
    assert s.nthMagicalNumber(10 ** 7, 5, 12) == s.nthMagicalNumberBisect(
        10 ** 7, 5, 12
    ) % MOD

    print("all good")
