import math
import random


class Solution:
    def maxValue(self, n, index, maxSum):
        # eleventh on the monotone-predicate-plus-bisect shape, and the first
        # where the predicate is O(1). every one of the previous ten had a scan
        # in it - a greedy on nine of them, a sum over the batteries on the
        # tenth - so evaluating the predicate cost a pass over the input and the
        # only thing you could do with it was call it.
        #
        # here it is a closed form. fix the peak value v; the cheapest legal
        # array with that peak is the clamped tent max(1, v - |i - index|), and
        # its sum is two arithmetic series with a clamp, which is arithmetic and
        # not a loop. see _minimum_sum.
        #
        # closed form has two consequences and they arrive together. the first is
        # that the predicate no longer builds anything, so the witness needs its
        # own construction - second day running, after ten days of getting it
        # free from the greedy. the second is the day's actual result: a closed
        # form can be *solved*. see maxValueDirect.
        left = index + 1
        right = n - index

        # bounds, seventh day.
        #
        # bottom: v = 1 is the all-ones array, sum n, and the constraints promise
        # n <= maxSum. so it is feasible by a promise in the statement rather
        # than by arithmetic - 1898's bottom end and not 2141's, and worth
        # separating because the promise is the thing that would quietly stop
        # being true if this were a subroutine somewhere.
        #
        # top: every entry is at least 1, so the other n - 1 of them cost at
        # least n - 1 and the peak cannot exceed maxSum - n + 1. a bound and not
        # a witness, again - it comes from discarding the tent's shape, and
        # discarding structure gives you a bound. third day running that the top
        # end is an upper bound with nothing achieving it, and after the 21st i
        # am no longer surprised by that; the surprise was the nine days before,
        # where the extreme threshold happened to be achievable every time.
        low, high = 1, maxSum - n + 1

        # maximization, so the true half keeps mid and mid rounds up. fifth
        # maximization in eleven, sixth day writing the rule out.
        while low < high:
            mid = (low + high + 1) // 2
            if self._minimum_sum(left, right, mid) <= maxSum:
                low = mid
            else:
                high = mid - 1

        return low

    def _minimum_sum(self, left, right, peak):
        """Sum of the cheapest legal array with `peak` at the index.

        `left` is the number of entries from position 0 through the index
        inclusive, `right` from the index through the end inclusive, so
        `left + right == n + 1` and the index is counted by both.

        The array is `max(1, peak - |i - index|)`, the tent that falls away by
        one per step and then flattens at the floor of 1. Each side is an
        arithmetic run, clamped or not depending on whether `peak` outlasts the
        side's length, and `_side_sum` does one side. The peak is subtracted once
        because both sides include it.

        `O(1)`. First predicate in the run that does not touch the input.
        """
        return (
            self._side_sum(left, peak) + self._side_sum(right, peak) - peak
        )

    def _side_sum(self, length, peak):
        """`sum(max(1, peak - d) for d in range(length))`, in closed form.

        Two regimes with the breakpoint at `peak == length`:

        - `peak >= length`: the run never reaches the floor. It is
          `peak, peak-1, ..., peak-length+1`, summing to
          `length * peak - length * (length - 1) / 2`. Linear in `peak`.
        - `peak < length`: the run hits 1 and stays there. It is
          `peak, peak-1, ..., 1` and then `length - peak` ones, summing to
          `peak * (peak + 1) / 2 + (length - peak)`. Quadratic in `peak`.

        Both halves are exact in integers - `length * (length - 1)` and
        `peak * (peak + 1)` are both even - so there is no rounding anywhere and
        no float in the primary path. `maxSum` reaches `1e9` and `length * peak`
        reaches `1e18`, which Python does not care about and which is the sort of
        thing that stops being true silently in a language that does.
        """
        if peak >= length:
            return length * peak - length * (length - 1) // 2

        return peak * (peak + 1) // 2 + (length - peak)

    def maxValueMinimalArray(self, n, index, peak):
        """The cheapest legal array with `peak` at the index - the witness.

        Seventeenth day of the summary-versus-set split, and the first canonical
        witness in the run.

        The two before this were both non-canonical and for the two different
        reasons the notes finally separated on the 20th and 21st: slack with no
        symmetry, where leftmost still named a member, and symmetry no rule could
        break. Today there is nothing to pick between, because there is exactly
        one thing to pick.

        Fix `peak` and let `S` be the set of legal arrays with that value at the
        index - positive integers, adjacent entries differing by at most one.
        `S` has a least element under the pointwise order, and it is this tent.

        The direct proof is two lines. Any `a` in `S` has `a[index] = peak`, and
        stepping one position changes the value by at most one, so
        `a[i] >= peak - |i - index|`; entries are positive, so `a[i] >= 1`; hence
        `a[i] >= max(1, peak - |i - index|)`. And the tent is itself in `S`. So it
        is below everything in `S` and is a member, which is what least means.

        The reason it works is worth naming, because the direct proof hides it.
        `S` is closed under pointwise minimum: positivity survives a min, and
        `|min(a_i, b_i) - min(a_j, b_j)| <= max(|a_i - a_j|, |b_i - b_j|) <= 1`
        for adjacent `i, j`, so the min of two legal arrays is legal. A nonempty
        set of positive integer arrays closed under meet has a least element. The
        canonicity is a lattice fact about the constraints, not a convention about
        how to break a tie, and that is a third thing "canonical" can mean on top
        of the two the 21st separated.

        **And it is why the predicate is a closed form.** Feasibility at `peak` is
        "some legal array with that peak has sum at most `maxSum`", which because
        sum is monotone in the pointwise order is "the least one does". So the
        predicate is `sum(least element) <= maxSum`, the least element is written
        down rather than searched for, and its sum is arithmetic. One property -
        meet-closure - giving the canonical witness and the `O(1)` predicate at
        the same time.

        `O(n)` to write out, which is the first honest cost in the file, and it is
        the witness's cost rather than the answer's.
        """
        return [max(1, peak - abs(i - index)) for i in range(n)]

    def maxValueDirect(self, n, index, maxSum):
        """The answer by inverting the predicate instead of searching it.

        `_minimum_sum` as a function of `peak` is piecewise polynomial with
        breakpoints where each side stops clamping, at `min(left, right)` and
        `max(left, right)`. Three pieces:

        - `peak <= lo`: both sides clamped. `peak**2 - 2*peak + left + right`.
        - `lo <= peak <= hi`: the short side is free, the long one clamped.
          `(peak**2 + (2*lo - 3) * peak + 2*hi - lo*(lo - 1)) / 2`.
        - `peak >= hi`: both free. `n * peak - (lo*(lo-1) + hi*(hi-1)) / 2`,
          using `left + right - 1 == n`.

        Each piece is a linear or quadratic inequality in one variable and every
        one of them can be solved. Take the root of each, keep the candidates that
        land in their own piece, and return the largest that passes the predicate.
        `O(1)`, no search of any kind.

        **This is the thing the eleven days were missing, and unlike the 21st it
        is inside the mathematics.**

        The framework says: the search space is generically bigger than the answer
        set, and which move you get depends on the answer set's size against the
        cost of the search it replaces. On the 21st that comparison turned out to
        be settled by the constraint format - `log(range)` capped by the width of
        a machine integer, `|answer set|` capped by nothing - so the result was
        decided before I opened the first problem, by the venue rather than by the
        problem. I wrote that night that I did not think the rule was wrong, only
        that I could not test it here, which was true and was also me not looking
        at the right thing.

        Both branches of that comparison are searches, and a search is what you do
        with a predicate you can only *call*. Ten days of predicates that were
        scans - a greedy placing balls, a sweep counting bouquets, a sum over
        batteries - and the only handle any of them offered was evaluation at a
        point. Bisection is the general method for exactly that situation and its
        cost is the price of having no other handle.

        This predicate is a formula, so it has another handle. Inverting it is not
        a cheaper search, it is not a search. And the axis that separates today
        from the previous ten is not the size of anything. It is whether the
        predicate is a black box or an expression, which is a property of the
        problem and not of the constraint block.

        Which also fixes the axis I proposed on the 21st. I said the question was
        whether membership in the answer set is decidable locally, on the strength
        of 2141's peel. That was the right observation with the wrong name on it -
        the peel worked because the predicate's structure was exposed, and local
        decidability was one symptom of that. The general statement is the one
        above, and "locally decidable" and "invertible" are two ways the structure
        can show up.

        The roots go through `math.isqrt` and floor division, which both round
        down, and I wrote this the first time with a `+/- 1` window around each
        candidate on the assumption that flooring twice loses one. It does not,
        and the reason is worth writing out because the assumption is the sort
        that never gets checked.

        For integer `c` and real `s >= 0`, `floor((c + s) / 2)` equals
        `(c + isqrt_of_s) // 2`. Let `m = floor((c + s) / 2)`. Then `2m - c <= s`,
        and `2m - c` is an integer, so `2m - c <= floor(s)`, so
        `m <= (c + floor(s)) / 2` and therefore `m <= floor((c + floor(s)) / 2)`.
        The other direction is `floor(s) <= s`. So the inner floor is free. Same
        argument covers `1 + isqrt(r)` and the plain `//` in the linear piece.

        The window came out and the equality is asserted at the bottom against a
        widened search, so the claim is tested rather than reasoned about once and
        trusted. Flooring an upper bound and flooring an answer are not the same
        operation even when the arithmetic looks identical, and here they happen
        to coincide - which is a fact about this expression and not a general
        licence.
        """
        left = index + 1
        right = n - index
        lo, hi = min(left, right), max(left, right)
        ceiling = maxSum - n + 1

        candidates = {1, ceiling, lo, hi}

        # both sides clamped: peak**2 - 2*peak + left + right <= maxSum, so
        # peak <= 1 + sqrt(1 + maxSum - left - right).
        radicand = 1 + maxSum - left - right
        if radicand >= 0:
            candidates.add(1 + math.isqrt(radicand))

        # one side free: peak**2 + (2*lo - 3)*peak + (2*hi - lo*(lo-1)) <= 2*maxSum.
        b = 2 * lo - 3
        c = 2 * hi - lo * (lo - 1) - 2 * maxSum
        discriminant = b * b - 4 * c
        if discriminant >= 0:
            candidates.add((-b + math.isqrt(discriminant)) // 2)

        # both sides free: n * peak - (lo*(lo-1) + hi*(hi-1))/2 <= maxSum.
        candidates.add((maxSum + (lo * (lo - 1) + hi * (hi - 1)) // 2) // n)

        best = 1
        for peak in candidates:
            if 1 <= peak <= ceiling and self._minimum_sum(left, right, peak) <= maxSum:
                best = max(best, peak)

        return best

    def maxValueEnd(self, n, maxSum):
        """The answer when the index is at either end, in one branch instead of three.

        With `index == 0` the left side is a single entry, `_side_sum(1, peak)` is
        just `peak`, and `_minimum_sum` collapses to `_side_sum(n, peak)` - one
        arithmetic run and no second breakpoint. The three pieces of
        `maxValueDirect` become two, and the mixed piece, which is the only one
        with a quadratic that needed care, disappears entirely.

        Same role as 2141's `n == 1` and 2616's `p == 1`: the input where a branch
        of the general code is dead, which makes it the cleanest thing to check
        the general path against. It is also the input that maximizes the answer
        for a given `n` and `maxSum`, since an end peak holds up one slope instead
        of two, so it is where the arithmetic runs largest and where an overflow
        would show first in a language that had them.

        By symmetry the same value answers `index == n - 1`.

        - `peak >= n`: `n * peak - n * (n - 1) / 2 <= maxSum`.
        - `peak < n`: `peak * (peak + 1) / 2 + n - peak <= maxSum`, so
          `peak <= (1 + sqrt(1 + 8 * maxSum - 8 * n)) / 2`.
        """
        free = (maxSum + n * (n - 1) // 2) // n
        if free >= n:
            return free

        clamped = (1 + math.isqrt(1 + 8 * maxSum - 8 * n)) // 2
        return max(1, min(clamped, n - 1))

    def maxValueByBisectOnWitness(self, n, index, maxSum):
        """Same answer, with the predicate evaluated by building the array.

        `sum(maxValueMinimalArray(...)) <= maxSum` instead of `_minimum_sum`. The
        two agree by construction - one is the closed form of the other - and the
        agreement is what tests the arithmetic in `_side_sum`, which is the only
        place in the file where a wrong constant would produce a plausible wrong
        answer rather than a crash.

        `O(n log(maxSum))`, which is what the previous ten cost and is here so
        that the cost of *not* having the closed form is a number in the file
        rather than a claim in a docstring. Kept for small inputs only.
        """
        low, high = 1, maxSum - n + 1

        while low < high:
            mid = (low + high + 1) // 2
            if sum(self.maxValueMinimalArray(n, index, mid)) <= maxSum:
                low = mid
            else:
                high = mid - 1

        return low


if __name__ == "__main__":
    s = Solution()

    assert s.maxValue(4, 2, 6) == 2
    assert s.maxValue(6, 1, 10) == 3
    assert s.maxValue(1, 0, 1) == 1
    assert s.maxValue(3, 0, 815094800) == 271698267
    assert s.maxValue(4, 0, 6) == 2
    assert s.maxValue(7, 3, 100) == 16
    assert s.maxValue(10, 0, 100) == 14

    cases = [
        (4, 2, 6),
        (6, 1, 10),
        (1, 0, 1),
        (4, 0, 6),
        (3, 2, 18),
        (5, 0, 5),
        (5, 4, 5),
        (5, 2, 5),
        (2, 0, 2),
        (2, 1, 3),
        (7, 3, 7),
        (7, 3, 100),
        (9, 4, 21),
        (10, 0, 100),
        (10, 9, 100),
        (3, 0, 815094800),
        (6, 1, 10),
        (1, 0, 1000000000),
    ]

    for n, index, max_sum in cases:
        assert 1 <= n <= max_sum, (n, index, max_sum)
        assert 0 <= index < n, (n, index, max_sum)

    # the two ends of the range, checked rather than asserted in prose. seventh
    # day of writing a bounds paragraph and the third of turning it into asserts.
    #
    # the bottom end is a point: v = 1 is the all-ones array and its sum is n,
    # which the constraints promise is at most maxSum. so it gets tested as a
    # witness.
    #
    # the top end is a bound and only a bound, same as the 21st. maxSum - n + 1
    # comes from throwing away the tent's shape and keeping only "every other
    # entry costs at least 1", and a discarded constraint gives an upper bound
    # rather than an achievable configuration. n=3, index=1, maxSum=6 has a
    # ceiling of 4 and an answer of 2, because a peak of 4 in the middle drags
    # its neighbours up to 3 each. so the point *above* the ceiling is what gets
    # tested, and the ceiling itself is only asserted to bound the answer.
    for n, index, max_sum in cases:
        left, right = index + 1, n - index
        assert s._minimum_sum(left, right, 1) <= max_sum, (n, index, max_sum)
        assert s._minimum_sum(left, right, max_sum - n + 2) > max_sum, (
            n,
            index,
            max_sum,
        )
        assert s.maxValue(n, index, max_sum) <= max_sum - n + 1, (n, index, max_sum)

    # the closed form against its own definition, computed the slow obvious way.
    # a predicate that is wrong but still monotone hands back a confident wrong
    # boundary and nothing downstream notices - the same reason the 21st brute
    # forced its work count.
    def minimum_sum_brute(n, index, peak):
        return sum(max(1, peak - abs(i - index)) for i in range(n))

    for n, index, max_sum in cases:
        if n > 200:
            continue
        for peak in range(1, 60):
            assert s._minimum_sum(index + 1, n - index, peak) == minimum_sum_brute(
                n, index, peak
            ), (n, index, peak)

    # monotonicity, in the direction the bisect uses.
    #
    # and this one comes from the witness, which is new. the previous ten read it
    # off a greedy - more budget, more room, the scan takes at least as many -
    # except the 21st, which had to go through concavity because both sides of
    # the inequality moved. here the least legal array is pointwise
    # non-decreasing in the peak, since max(1, v - d) is, so its sum is too, so
    # the feasible set is a prefix. monotonicity of the canonical witness handed
    # straight to the predicate.
    #
    # strictly increasing, in fact, since the entry at the index is the peak
    # itself. so there is no plateau and the boundary is a single point rather
    # than the top of a flat stretch.
    for n, index, max_sum in cases:
        if n > 200:
            continue
        sums = [s._minimum_sum(index + 1, n - index, peak) for peak in range(1, 80)]
        assert all(a < b for a, b in zip(sums, sums[1:])), (n, index)

    # the witness is real and it is the least one. every entry positive, adjacent
    # entries within one, the peak where it is claimed, sum inside the budget -
    # and then the least-element claim itself, checked against every legal array
    # on the small cases rather than trusted from the docstring.
    for n, index, max_sum in cases:
        peak = s.maxValue(n, index, max_sum)
        array = s.maxValueMinimalArray(n, index, peak)

        assert len(array) == n
        assert array[index] == peak
        assert all(value >= 1 for value in array), (n, index, array)
        assert all(abs(a - b) <= 1 for a, b in zip(array, array[1:])), (n, index, array)
        assert sum(array) <= max_sum, (n, index, max_sum, sum(array))

    # the least-element claim, by enumeration. build every legal array of the
    # given length with the given value at the index and check the tent is
    # pointwise below all of them. this is the only check in the file that does
    # not go through _minimum_sum at all, so it tests the lattice argument rather
    # than restating it.
    def legal_arrays(n, index, peak, ceiling):
        def extend(prefix):
            position = len(prefix)
            if position == n:
                if prefix[index] == peak:
                    yield tuple(prefix)
                return

            if position == index:
                lower = upper = peak
            else:
                lower, upper = 1, ceiling

            if prefix:
                lower = max(lower, prefix[-1] - 1)
                upper = min(upper, prefix[-1] + 1)

            for value in range(lower, upper + 1):
                yield from extend(prefix + [value])

        return extend([])

    for n, index, peak in ((4, 2, 3), (5, 0, 2), (3, 1, 3), (5, 2, 1), (4, 3, 2)):
        tent = s.maxValueMinimalArray(n, index, peak)
        seen = 0
        for array in legal_arrays(n, index, peak, peak + 2):
            seen += 1
            assert all(a <= b for a, b in zip(tent, array)), (n, index, peak, array)
        assert seen > 1, (n, index, peak)
        assert tuple(tent) in set(legal_arrays(n, index, peak, peak + 2))

    # the answer is maximal - one more is infeasible. stated directly rather than
    # inferred from the bisect, since the bisect would report the same thing if
    # the predicate were wrong.
    for n, index, max_sum in cases:
        peak = s.maxValue(n, index, max_sum)
        assert minimum_sum_brute(n, index, peak) <= max_sum or n > 200, (n, index)
        assert s._minimum_sum(index + 1, n - index, peak + 1) > max_sum, (
            n,
            index,
            max_sum,
        )

    # the inversion agrees with the search. it shares the predicate but not the
    # search, so agreement tests the algebra in maxValueDirect - three pieces,
    # three roots, and the isqrt rounding that cost me a wrong answer on
    # (4, 0, 6) before the +/- 1 window went in.
    for n, index, max_sum in cases:
        assert s.maxValueDirect(n, index, max_sum) == s.maxValue(n, index, max_sum), (
            n,
            index,
            max_sum,
        )

    # and the predicate built the slow way agrees with the closed form, which is
    # what tests _side_sum's constants.
    for n, index, max_sum in cases:
        if n > 50 or max_sum > 10000:
            continue
        assert s.maxValueByBisectOnWitness(n, index, max_sum) == s.maxValue(
            n, index, max_sum
        ), (n, index, max_sum)

    # the end-index shortcut, where the mixed piece of the closed form is dead
    # code. both ends, since the symmetry claim is part of what it asserts.
    for n, index, max_sum in cases:
        assert s.maxValueEnd(n, max_sum) == s.maxValue(n, 0, max_sum), (n, max_sum)
        assert s.maxValueEnd(n, max_sum) == s.maxValue(n, n - 1, max_sum), (n, max_sum)

    # the roots are exact without a window, which is the claim in maxValueDirect's
    # docstring and the one I had wrong first. searching a window of five around
    # every candidate must find nothing the bare roots missed - if flooring twice
    # ever lost one, this is where it would show.
    def direct_windowed(n, index, max_sum):
        left, right = index + 1, n - index
        ceiling = max_sum - n + 1
        best = 1
        for centre in (s.maxValueDirect(n, index, max_sum),):
            for peak in range(centre - 2, centre + 3):
                if 1 <= peak <= ceiling and s._minimum_sum(left, right, peak) <= max_sum:
                    best = max(best, peak)
        return best

    for n, index, max_sum in cases:
        assert direct_windowed(n, index, max_sum) == s.maxValueDirect(
            n, index, max_sum
        ), (n, index, max_sum)

    # every index on the same (n, maxSum), so the boundary is walked across
    # rather than sampled. the answer is largest at an end and smallest in the
    # middle, because an interior peak has two sides to hold up and an end peak
    # has one - which is monotone in the distance to the nearer end, and nothing
    # else here would catch that failing.
    for n, max_sum in ((9, 40), (8, 30), (12, 60), (7, 200)):
        answers = [s.maxValue(n, index, max_sum) for index in range(n)]
        assert answers[0] == answers[-1], (n, max_sum, answers)
        assert answers[0] == max(answers), (n, max_sum, answers)
        assert answers[n // 2] == min(answers), (n, max_sum, answers)

        for index in range(n):
            assert s.maxValueDirect(n, index, max_sum) == answers[index]
            assert answers[index] == answers[n - 1 - index], (n, max_sum, answers)

    # random cases across all three implementations. the fixed cases are all
    # hand-picked for a reason and hand-picked cases stop finding things once
    # they pass once.
    rng = random.Random(1802)
    for _ in range(600):
        n = rng.randint(1, 40)
        index = rng.randrange(n)
        max_sum = rng.randint(n, n + rng.randint(0, 3000))

        answer = s.maxValue(n, index, max_sum)
        assert s.maxValueDirect(n, index, max_sum) == answer, (n, index, max_sum)
        assert s.maxValueByBisectOnWitness(n, index, max_sum) == answer, (
            n,
            index,
            max_sum,
        )
        assert minimum_sum_brute(n, index, answer) <= max_sum, (n, index, max_sum)
        assert minimum_sum_brute(n, index, answer + 1) > max_sum, (n, index, max_sum)

    # and at the constraint ceiling, because everything above is small enough
    # that the inversion and the bisect cost the same and the whole argument in
    # today's note is about what happens when they do not.
    for n, index, max_sum in (
        (1, 0, 10 ** 9),
        (10 ** 9, 0, 10 ** 9),
        (10 ** 9, 999999999, 10 ** 9),
        (10 ** 9, 500000000, 10 ** 9),
        (2, 1, 10 ** 9),
        (100000, 50000, 10 ** 9),
        (100000, 0, 10 ** 9),
    ):
        answer = s.maxValue(n, index, max_sum)
        assert s.maxValueDirect(n, index, max_sum) == answer, (n, index, max_sum)
        assert s._minimum_sum(index + 1, n - index, answer) <= max_sum
        assert s._minimum_sum(index + 1, n - index, answer + 1) > max_sum
        if index in (0, n - 1):
            assert s.maxValueEnd(n, max_sum) == answer, (n, index, max_sum)

    print("all good")
