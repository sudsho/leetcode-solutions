import heapq
import math
from fractions import Fraction


class Solution:
    def minmaxGasDist(self, stations, k):
        # sixth day on the monotone-predicate-plus-bisect shape, and the first
        # one where the answer is not an integer. i expected that to be a detail
        # about the loop condition. it is not - it changes what the bisect is
        # allowed to claim, and it changes it in the one direction i would not
        # have guessed.
        #
        # the setup is the same as always. adding a station only ever shortens a
        # gap, so the number of stations needed to bring every gap under x is
        # non-increasing in x, needed(x) <= k is upward closed, bisect for the
        # boundary. nothing new there.
        #
        # what is new is that the boundary is a real number and the search space
        # is the reals. three things break, and only the first is the one people
        # warn about:
        #
        # 1. termination stops being free. on the integer lattice low = mid + 1
        #    strictly shrinks the range every iteration, so the loop terminating
        #    was a proof and not a hope. on floats mid can round to low, and then
        #    low = mid moves nothing and it spins. five days of `while low <
        #    high` and i never once had to think about progress.
        #
        # 2. the answer is no longer a point of the search space that i can
        #    return. i return an endpoint of a bracket and claim the true answer
        #    is inside it. correctness became a tolerance claim.
        #
        # 3. and this is the day. the predicate is allowed to be wrong now. on
        #    integers every point of the search space had weight, so a predicate
        #    that misfired at one value moved the boundary by one and that was a
        #    wrong answer. here the boundary is a limit of the feasible set, so
        #    the predicate can be wrong on any measure-zero set without moving it
        #    at all. the floor-based count below is wrong at exactly the
        #    multiples, which is measure zero, which is why every implementation
        #    of this that uses it is correct anyway. same substitution, fatal in
        #    one setting and free in the other, and what decides which is whether
        #    points have weight.
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        if not gaps:
            return 0.0

        low, high = 0.0, float(max(gaps))

        # fixed count rather than `while high - low > 1e-6`. the eps form does
        # terminate here - 1e-6 at a magnitude of 1e8 is still four orders above
        # the ulp - but it terminates because of the constraint on the
        # coordinates and not because of anything in the algorithm, and i would
        # rather the loop not lean on that. 100 halvings takes 1e8 down to 1e-22,
        # which saturates the double long before it runs out, so the tail
        # iterations are no-ops and cost nothing.
        for _ in range(100):
            mid = (low + high) / 2
            if self._stations_needed(gaps, mid, cap=k) <= k:
                high = mid
            else:
                low = mid

        return high

    def _stations_needed(self, gaps, limit, cap=math.inf):
        """Stations to add so that every gap is at most `limit`.

        Splitting a gap of `d` into pieces no longer than `limit` takes
        `ceil(d / limit)` pieces and so `ceil(d / limit) - 1` new stations. The
        gaps are independent - a station dropped in one does nothing for any
        other - so the total is the sum, with no allocation question hiding
        inside it.

        That puts this next to 2064's ceiling sum rather than next to 2528 and
        1552, where the predicate had a greedy in it and the exchange argument
        was most of the work. Four of the six now have a trivial inner predicate,
        which keeps pointing at the same conclusion: the variation in this shape
        lives in what the predicate *is*, and not in how it gets answered.

        `cap` stops the sum once the answer can no longer change. That is not
        only speed - as `limit` goes to zero the count goes to infinity, and
        bounding it means the return value is a decision rather than a number
        that can be astronomically large for reasons unrelated to the answer.
        Left as `inf` by default so the tests can check the plain definition.
        """
        if limit <= 0:
            return math.inf

        needed = 0
        for d in gaps:
            needed += math.ceil(d / limit) - 1
            if needed > cap:
                break

        return needed

    def _stations_needed_floor(self, gaps, limit):
        """The count everyone writes: `floor(d / limit)` summed over the gaps.

        Kept because the disagreement with `_stations_needed` is the day's
        subject, and I would rather have it in the file than in a comment.

        `floor(y)` and `ceil(y) - 1` are the same number unless `y` is an
        integer, where floor is one larger. So this over-counts on exactly the
        limits that divide some gap evenly, and over-counting means calling
        infeasible something that is feasible. The floor-feasible set is
        `(answer, inf)` where the true one is `[answer, inf)`: the one point it
        gets wrong is the correct endpoint itself.

        Which does not matter, and the reason it does not matter is the point.
        The bisect never returns a member of the feasible set. It returns a
        bracket around the infimum, and a set and its closure have the same
        infimum. Half-open at a single point is invisible to a limit.
        """
        if limit <= 0:
            return math.inf

        return sum(int(d / limit) for d in gaps)

    def minmaxGasDistExact(self, stations, k):
        """The exact answer as a `Fraction`, by greedy splitting instead of search.

        Whatever the final allocation is, it hands `c_i` new stations to gap `i`
        and splits it evenly, so the penalty is `max_i d_i / (c_i + 1)` over the
        allocations with `sum c_i = k`. Giving the next station to whichever gap
        currently has the largest `d_i / (c_i + 1)` is optimal by exchange: that
        gap attains the current maximum, no station placed anywhere else lowers
        it, so any allocation that never feeds it is beaten by one that does.

        The reason to keep this rather than call it a second solution is that it
        shares nothing with the bisect. No predicate, no monotonicity claim, no
        bounds, and no floating point - the keys are `Fraction`s and the heap
        compares them exactly. So when it agrees with the bisect to within the
        tolerance that is evidence about the bisect, and not a restatement of it.
        Several days in this run kept alternates that shared their inner loop
        with the primary, and I had been counting that agreement as a
        cross-check when it mostly was not one.

        It is also slower exactly where it matters. `k` runs to a million and
        this does a pop and a push per station, against the bisect's hundred
        passes over at most two thousand gaps, with exact arithmetic making the
        constant worse on top of that.
        """
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        if not gaps:
            return Fraction(0)

        # max-heap on the current piece length, so the key is negated
        heap = [(-Fraction(d), d, 1) for d in gaps]
        heapq.heapify(heap)

        for _ in range(k):
            _, d, pieces = heapq.heappop(heap)
            pieces += 1
            heapq.heappush(heap, (-Fraction(d, pieces), d, pieces))

        return -heap[0][0]

    def minmaxGasDistWitness(self, stations, k):
        """Return `(penalty, counts)` with `counts[i]` stations added to gap `i`.

        Twelfth day of the summary-versus-set split and the fourth straight
        non-canonical witness, which by now is the expectation rather than the
        observation. What is worth writing down is *which* of the three reasons
        it is, because yesterday ended on slack being the generic case and
        symmetry and multiplicity being the special ones, and this is the first
        chance to check that against a new problem.

        It is slack, in the most literal form so far: stations that change
        nothing. Two gaps of 10 with `k = 1` give a penalty of 10 whichever gap
        the station goes in, because the untouched one sets the maximum either
        way. The station is not merely reallocatable, it is inert. Same shape as
        2528's unspent budget and 2064's unused stores, so three problems in this
        run have now had a resource the objective cannot see, always for the same
        reason - the objective reads a max, and a max ignores everything that is
        not the argmax.

        So the tests check `sum(counts) == k` and that the counts realize the
        penalty, and nothing at all about which gaps they land in.
        """
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        if not gaps:
            return Fraction(0), []

        heap = [(-Fraction(d), d, 1, i) for i, d in enumerate(gaps)]
        heapq.heapify(heap)

        for _ in range(k):
            _, d, pieces, i = heapq.heappop(heap)
            pieces += 1
            heapq.heappush(heap, (-Fraction(d, pieces), d, pieces, i))

        counts = [0] * len(gaps)
        for _key, _d, pieces, i in heap:
            counts[i] = pieces - 1

        return -heap[0][0], counts

    def minmaxGasDistSingleGap(self, stations, k):
        """Shortcut for two stations: the answer is `d / (k + 1)`, no search.

        One gap leaves nothing to allocate, so every station lands in it and the
        even split is forced. No predicate, no greedy, no bisect.

        Same role as 1482's `k == 1` and 719's adjacent-minimum shortcut - the
        input on which the algorithm makes no decisions, which makes it the
        cleanest thing to check the general path against. It earns the place
        twice over here, because it is the only check that pins the arithmetic
        to a closed form rather than to another search, and because `d / (k + 1)`
        with `k` large is where the answer sits smallest relative to the range
        and the bisect has the furthest to travel to reach it.

        Returns `None` when it does not apply, so it cannot be used by accident.
        """
        if len(stations) != 2:
            return None

        return Fraction(stations[1] - stations[0], k + 1)


if __name__ == "__main__":
    s = Solution()

    TOL = 1e-6

    assert abs(s.minmaxGasDist([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9) - 0.5) < TOL
    assert abs(s.minmaxGasDist([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1) - 14.0) < TOL
    assert abs(s.minmaxGasDist([0, 100], 1) - 50.0) < TOL
    assert abs(s.minmaxGasDist([0, 100], 3) - 25.0) < TOL

    cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9),
        ([23, 24, 36, 39, 46, 56, 57, 65, 84, 98], 1),
        ([0, 100], 1),
        ([0, 100], 3),
        ([0, 10, 20], 1),
        ([0, 10, 20], 2),
        ([0, 10, 20], 5),
        ([0, 1, 100], 1),
        ([0, 1, 100], 10),
        ([0, 3, 9, 10, 30], 4),
        ([0, 2, 4, 6, 8], 7),
        ([5, 6], 1),
        ([0, 1000000], 999),
        ([0, 7, 8, 9, 40, 41], 6),
        ([10, 11, 12, 13, 14, 15], 3),
    ]

    # the exact greedy shares no predicate, no bounds and no float with the
    # bisect, so agreement is evidence rather than a restatement
    for stations, k in cases:
        exact = s.minmaxGasDistExact(stations, k)
        assert abs(s.minmaxGasDist(stations, k) - float(exact)) < TOL, (stations, k, exact)

    # the answer is always d / j for some gap d and some 1 <= j <= k+1, so on
    # small inputs the entire candidate set can be enumerated and the smallest
    # feasible one taken. exact, and independent of both the bisect and the
    # greedy. it is also the direct contrast with yesterday - 1482's candidate
    # set was the input itself, small enough to bisect over, and this one has
    # |gaps| * (k+1) elements and runs to two billion at the constraint ceiling.
    # the answer being attained does not make it enumerable.
    def brute(stations, k):
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        candidates = sorted({Fraction(d, j) for d in gaps for j in range(1, k + 2)})
        for x in candidates:
            if sum(math.ceil(Fraction(d) / x) - 1 for d in gaps) <= k:
                return x
        raise AssertionError("no candidate was feasible")

    small_cases = [(st, k) for st, k in cases if k <= 30 and len(st) <= 8]

    for stations, k in small_cases:
        assert s.minmaxGasDistExact(stations, k) == brute(stations, k), (stations, k)

    # the predicate against its definition, rather than through the search. a
    # count that is wrong but still monotone gives a confident wrong boundary
    # with no symptom, which is the thing 1482 ended on. the limits are halves so
    # they are exact doubles and the comparison is not testing the rounding.
    for stations, _ in small_cases:
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        for half in range(1, 2 * max(gaps) + 3):
            limit = half / 2
            by_hand = 0
            for d in gaps:
                pieces = 1
                while d / pieces > limit:
                    pieces += 1
                by_hand += pieces - 1
            assert s._stations_needed(gaps, limit) == by_hand, (stations, limit)

    # monotonicity, which every one of these searches assumes and none of them
    # would notice failing
    for stations, _ in small_cases:
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        counts = [s._stations_needed(gaps, half / 2)
                  for half in range(1, 2 * max(gaps) + 3)]
        assert all(a >= b for a, b in zip(counts, counts[1:])), stations

    # the two predicates disagree pointwise on exactly the limits that divide
    # some gap evenly - stated as a fact about the pair, not inferred from the
    # two searches happening to agree
    for gaps in [[10, 6], [12, 8, 4], [7], [100, 25]]:
        disagreed = [limit for limit in range(1, 26)
                     if s._stations_needed_floor(gaps, float(limit))
                     != s._stations_needed(gaps, float(limit))]
        assert disagreed == [limit for limit in range(1, 26)
                             if any(d % limit == 0 for d in gaps)], gaps
        for limit in range(1, 26):
            assert (s._stations_needed_floor(gaps, float(limit))
                    >= s._stations_needed(gaps, float(limit))), (gaps, limit)

    # and the disagreement is invisible to the bisect, which is the claim the
    # whole day rests on. same search, wrong predicate, same limit.
    def solve_with_floor(stations, k):
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        low, high = 0.0, float(max(gaps))
        for _ in range(100):
            mid = (low + high) / 2
            if s._stations_needed_floor(gaps, mid) <= k:
                high = mid
            else:
                low = mid
        return high

    for stations, k in cases:
        assert abs(s.minmaxGasDist(stations, k) - solve_with_floor(stations, k)) < TOL, (
            stations,
            k,
        )

    # the witness is one of possibly many optimal allocations, so it gets checked
    # on the property: k stations placed, and the even splits they induce realize
    # the penalty
    for stations, k in cases:
        penalty, counts = s.minmaxGasDistWitness(stations, k)
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        assert len(counts) == len(gaps), (stations, k)
        assert sum(counts) == k, (stations, k, counts)
        assert all(c >= 0 for c in counts), (stations, k, counts)
        assert max(Fraction(d, c + 1) for d, c in zip(gaps, counts)) == penalty, (
            stations,
            k,
            counts,
        )
        assert penalty == s.minmaxGasDistExact(stations, k), (stations, k)

    # inert stations: two equal gaps and one station, so the penalty is the
    # untouched gap whichever side it goes. written out rather than left to the
    # property check above, because "the witness is not canonical" and "the
    # resource does nothing" are different statements and this run has now run
    # them together three times.
    penalty, counts = s.minmaxGasDistWitness([0, 10, 20], 1)
    assert penalty == 10
    assert sorted(counts) == [0, 1]
    assert s.minmaxGasDistExact([0, 10, 20], 0) == 10

    # one gap removes every decision, so the general path has to agree with a
    # closed form. the greedy is skipped on the large-k rows since it is linear
    # in k and this is the only place k gets near the constraint ceiling, which
    # is itself the point of keeping the bisect as the primary.
    for stations, k in [([0, 100], 1), ([0, 100], 3), ([5, 6], 1), ([0, 1000000], 999),
                        ([3, 4], 999999), ([0, 100000000], 1000000)]:
        shortcut = s.minmaxGasDistSingleGap(stations, k)
        assert abs(s.minmaxGasDist(stations, k) - float(shortcut)) < TOL, (stations, k)
        if k <= 1000:
            assert s.minmaxGasDistExact(stations, k) == shortcut, (stations, k)

    assert s.minmaxGasDistSingleGap([0, 1, 2], 3) is None

    # the bracket is what gets returned, so its width is part of the claim, and
    # the true answer has to be inside it. this is the assert that catches the
    # iteration count being cut to something that merely looks sufficient.
    for stations, k in cases:
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        low, high = 0.0, float(max(gaps))
        for _ in range(100):
            mid = (low + high) / 2
            if s._stations_needed(gaps, mid, cap=k) <= k:
                high = mid
            else:
                low = mid
        exact = s.minmaxGasDistExact(stations, k)
        assert high - low < 1e-9, (stations, k, high - low)
        assert low <= float(exact) <= high + 1e-9, (stations, k, exact)

    print("all good")
