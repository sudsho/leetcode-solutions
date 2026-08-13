import bisect


class Solution:
    def minDays(self, bloomDay, m, k):
        # fifth day on the monotone-predicate-plus-bisect shape. four days of
        # notes have ended on some version of "the bounds came off the structure
        # and needed no guard", and i had started reading that as a property of
        # the technique. it isn't. today it breaks, and the way it breaks is the
        # day.
        #
        # every previous problem in this run was feasible somewhere. 2528 could
        # always power every city if the budget went far enough, 1552 could
        # always separate two balls, 2064 degenerated to one product per store,
        # 719 had a multiset that certainly contained a k-th element. so the
        # predicate was true at the top of the range by construction and the
        # only question was where it turned on.
        #
        # here it can be false everywhere. m bouquets of k adjacent flowers need
        # m*k flowers, and if the garden doesn't have that many, no amount of
        # waiting produces them. waiting only ever blooms flowers; it never adds
        # any. so the predicate is still monotone - it just may be constant
        # false, and a monotone predicate that never turns on has no boundary
        # for a bisect to find.
        #
        # the reason this is worth a whole day rather than a line: the failure is
        # silent. run the bisect anyway and low converges to high = max(bloomDay)
        # and gets returned as an answer. it's a real-looking number, it's in
        # range, nothing raises. every previous bug in this run announced itself
        # - a wrong bound gave an empty range or an out-of-bounds index. this one
        # just lies. "the search space is nonempty" and "the answer exists" are
        # different claims and i'd been getting the second for free from the
        # first for four days without noticing i was doing it.
        n = len(bloomDay)
        if m * k > n:
            return -1

        # and past that guard the range is not just nonempty, it's tight at both
        # ends. min(bloomDay) is the first day anything at all is open, so
        # nothing below it can be feasible. max(bloomDay) is the day the whole
        # garden is open, which is feasible precisely because the guard above
        # already ruled out the case where even the full garden isn't enough.
        # the guard isn't a special case bolted on the side - it's what makes
        # the upper bound correct.
        low, high = min(bloomDay), max(bloomDay)

        while low < high:
            mid = (low + high) // 2
            if self._bouquets_by(bloomDay, mid, k) >= m:
                high = mid
            else:
                low = mid + 1

        return low

    def _bouquets_by(self, bloomDay, day, k):
        """How many bouquets can be cut on `day`, greedily, left to right?

        A bouquet is `k` adjacent flowers that have all bloomed. Walk the array
        tracking the current run of open flowers, and every time the run reaches
        `k`, cut a bouquet and reset the run to zero.

        The greedy needs an argument and it's the shortest one in the run so far.
        Within a maximal run of `L` open flowers the answer is `L // k` no matter
        how the bouquets are placed, since each consumes exactly `k` and they
        can't overlap. So there's nothing to choose - cutting as early as
        possible reaches the same count as any other packing. Contrast 2528 and
        1552, where the greedy inside the predicate was doing real work and the
        exchange argument was the hard part. Here the predicate is closer to
        2064's ceiling sum: a formula wearing a loop.
        """
        bouquets = 0
        run = 0

        for bloom in bloomDay:
            if bloom <= day:
                run += 1
                if run == k:
                    bouquets += 1
                    run = 0
            else:
                run = 0

        return bouquets

    def minDaysOverValues(self, bloomDay, m, k):
        """Same answer, bisecting the distinct bloom days instead of the integers.

        Yesterday ended on the search range being strictly larger than the set of
        possible answers - 719 bisected `[0, max - min]` where most integers were
        not distances between any two elements - and the gap was repaired after
        the fact by the boundary being a jump in the count.

        Here the two sets can be made to coincide. The bloomed set only changes
        on days when something blooms, so the predicate is constant between
        consecutive distinct values of `bloomDay` and the answer is always one of
        them. Bisecting over the sorted distinct values directly makes the
        attainment question disappear rather than answering it, and drops the
        step count from `log(max value)` to `log(n)`.

        Kept as the alternate rather than the primary because the integer bisect
        is what generalizes - it needs nothing but monotonicity, whereas this
        needs the predicate to be piecewise constant with the pieces known in
        advance. That is a real property of this problem and not of the shape.
        Worth having both side by side for exactly that reason: they answer the
        same question and only one of them is the technique.
        """
        if m * k > len(bloomDay):
            return -1

        days = sorted(set(bloomDay))

        low, high = 0, len(days) - 1
        while low < high:
            mid = (low + high) // 2
            if self._bouquets_by(bloomDay, days[mid], k) >= m:
                high = mid
            else:
                low = mid + 1

        return days[low]

    def minDaysWitness(self, bloomDay, m, k):
        """Return `(day, starts)` where `starts` are the left ends of `m` bouquets.

        Eleventh day of the summary-versus-set split and the first repeated
        reason for the witness not being canonical. 1552 was symmetry, 2064 was
        slack, 719 was multiplicity, and this one is slack again - a maximal run
        of `L` open flowers with `L % k != 0` has spare flowers, so the bouquets
        can slide within the run, and any `m` of the available cuts will do.

        The repeat is the observation. Three days of distinct reasons had me
        half-expecting a new one each time, as if the reasons were a list being
        enumerated. Slack is just the generic case: whenever the objective reads
        a threshold rather than the whole assignment, whatever the assignment has
        left over is free. Symmetry and multiplicity were the special ones.

        So this returns the leftmost-greedy cut and stops at `m`, and the tests
        check the property - `m` bouquets, disjoint, all flowers open by the
        returned day - rather than the particular set.
        """
        day = self.minDays(bloomDay, m, k)
        if day == -1:
            return -1, []

        starts = []
        run = 0

        for i, bloom in enumerate(bloomDay):
            if bloom <= day:
                run += 1
                if run == k:
                    starts.append(i - k + 1)
                    run = 0
                    if len(starts) == m:
                        break
            else:
                run = 0

        # unreachable - `day` is feasible, so the greedy count reaches `m`.
        # raising rather than returning short, because falling through here
        # would mean the predicate and this scan disagree about the same day.
        if len(starts) != m:
            raise AssertionError("feasible day did not yield m bouquets")

        return day, starts

    def minDaysSingleFlower(self, bloomDay, m, k):
        """Shortcut for `k == 1`: the answer is the `m`-th smallest bloom day.

        With bouquets of one flower, adjacency says nothing and the count on day
        `d` is just how many flowers have opened. So feasibility is
        `#{bloom <= d} >= m`, and the smallest such `d` is the `m`-th order
        statistic. No search, and no greedy either.

        Same role as 719's adjacent-minimum shortcut: the input where the
        algorithm makes no decisions at all, which makes it the cleanest thing to
        check the general path against. It also pins the `low = min(bloomDay)`
        end, since `m = 1, k = 1` lands exactly on it and that is the one
        boundary the random cases never touch.

        Returns `None` when the shortcut does not apply, so it can't be used by
        accident on an input it says nothing about.
        """
        if k != 1:
            return None
        if m > len(bloomDay):
            return -1

        return sorted(bloomDay)[m - 1]


if __name__ == "__main__":
    s = Solution()

    assert s.minDays([1, 10, 3, 10, 2], 3, 1) == 3
    assert s.minDays([1, 10, 3, 10, 2], 3, 2) == -1
    assert s.minDays([7, 7, 7, 7, 12, 7, 7], 2, 3) == 12
    assert s.minDays([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2) == 9
    assert s.minDays([1000000000, 1000000000], 1, 1) == 1000000000

    cases = [
        ([1, 10, 3, 10, 2], 3, 1),
        ([1, 10, 3, 10, 2], 3, 2),
        ([7, 7, 7, 7, 12, 7, 7], 2, 3),
        ([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2),
        ([1000000000, 1000000000], 1, 1),
        ([5], 1, 1),
        ([5], 2, 1),
        ([5], 1, 2),
        ([1, 1, 1, 1, 1], 5, 1),
        ([1, 1, 1, 1, 1], 1, 5),
        ([1, 1, 1, 1, 1], 2, 3),
        ([3, 1, 4, 1, 5, 9, 2, 6], 2, 2),
        ([2, 2, 2, 2, 2, 2, 2, 2], 4, 2),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], 3, 3),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3),
        ([11, 5, 5, 11, 5, 5, 11], 2, 2),
    ]

    # the infeasible branch is the day's subject, so it gets checked as a branch
    # and not only as an output. m*k > n is the whole condition - it does not
    # depend on the bloom days at all, which is the thing that makes it a guard
    # on the range rather than a case inside the search.
    for bloomDay, m, k in cases:
        expected_feasible = m * k <= len(bloomDay)
        assert (s.minDays(bloomDay, m, k) != -1) == expected_feasible, (bloomDay, m, k)

    # the value-space bisect shares the predicate but not the range, so agreement
    # checks that the integer search really does land on a realized bloom day
    for bloomDay, m, k in cases:
        assert s.minDaysOverValues(bloomDay, m, k) == s.minDays(bloomDay, m, k), (
            bloomDay,
            m,
            k,
        )

    # and the answer is one of the bloom days whenever it exists, stated directly
    # rather than inferred from the two searches agreeing
    for bloomDay, m, k in cases:
        answer = s.minDays(bloomDay, m, k)
        if answer != -1:
            assert answer in bloomDay, (bloomDay, m, k, answer)

    # the witness is one of possibly many valid cuts, so it is checked on the
    # property: m bouquets, pairwise disjoint, every flower in them open by the
    # returned day
    for bloomDay, m, k in cases:
        day, starts = s.minDaysWitness(bloomDay, m, k)
        assert day == s.minDays(bloomDay, m, k), (bloomDay, m, k)
        if day == -1:
            assert starts == []
            continue
        assert len(starts) == m, (bloomDay, m, k, starts)
        used = set()
        for start in starts:
            window = range(start, start + k)
            assert start >= 0 and start + k <= len(bloomDay), (bloomDay, start)
            assert all(bloomDay[i] <= day for i in window), (bloomDay, m, k, start)
            assert used.isdisjoint(window), (bloomDay, m, k, starts)
            used.update(window)

    # k == 1 removes the greedy entirely, so the general path has to agree with a
    # plain order statistic. this is also the only check that touches the
    # low = min(bloomDay) end of the range.
    for bloomDay, m in [([1, 10, 3, 10, 2], 3), ([5], 1), ([5], 2), ([9, 8, 7], 1),
                        ([1, 1, 1, 1, 1], 5), ([4, 4, 2, 2, 9], 4)]:
        assert s.minDays(bloomDay, m, 1) == s.minDaysSingleFlower(bloomDay, m, 1), (
            bloomDay,
            m,
        )

    assert s.minDaysSingleFlower([1, 2, 3], 2, 2) is None

    # anything that walks the days one at a time is restricted to the gardens
    # whose bloom days are small. the constraint allows 1e9 and the checks below
    # are O(max bloom day) by design - that gap between what the search costs and
    # what verifying it costs is the reason the search exists at all.
    small_cases = [case for case in cases if max(case[0]) <= 20]

    # the counting pass against its definition. a predicate that is wrong but
    # still monotone gives a confident wrong boundary with no symptom, which was
    # yesterday's lesson and is why this is checked directly rather than through
    # the search.
    def bouquets_brute(bloomDay, day, k):
        open_flags = [bloom <= day for bloom in bloomDay]
        total = 0
        run = 0
        for flag in open_flags:
            run = run + 1 if flag else 0
            if run and run % k == 0:
                total += 1
        return total

    for bloomDay, _, k in small_cases:
        for day in range(0, max(bloomDay) + 2):
            assert s._bouquets_by(bloomDay, day, k) == bouquets_brute(bloomDay, day, k), (
                bloomDay,
                day,
                k,
            )

    # monotonicity of the predicate itself, which every one of these searches
    # assumes and none of them would notice failing
    for bloomDay, _, k in small_cases:
        counts = [s._bouquets_by(bloomDay, day, k) for day in range(0, max(bloomDay) + 2)]
        assert all(a <= b for a, b in zip(counts, counts[1:])), (bloomDay, k)

    # linear scan over every day up to the maximum, taking the first feasible
    # one. no bisect, no bounds, no guard - so it disagrees with the primary
    # exactly where the guard would have been missing.
    def brute(bloomDay, m, k):
        for day in range(0, max(bloomDay) + 1):
            if bouquets_brute(bloomDay, day, k) >= m:
                return day
        return -1

    for bloomDay, m, k in small_cases:
        assert s.minDays(bloomDay, m, k) == brute(bloomDay, m, k), (bloomDay, m, k)

    # every (m, k) on a handful of gardens, so the feasible/infeasible boundary
    # is walked across rather than sampled. the m*k = n corner - exactly enough
    # flowers and no slack - is the one the hand-written cases keep missing.
    for bloomDay in [[1, 10, 3, 10, 2], [7, 7, 7, 7, 12, 7, 7], [3, 1, 4, 1, 5, 9],
                     [2, 2, 2, 2], [1, 2, 3, 4, 5, 6]]:
        n = len(bloomDay)
        for m in range(1, n + 2):
            for k in range(1, n + 2):
                assert s.minDays(bloomDay, m, k) == brute(bloomDay, m, k), (bloomDay, m, k)

    # bisect is imported for the value-space search's neighbours; assert the
    # answer really is where bisect_left would put it among the distinct days,
    # which is the same claim as "the predicate is piecewise constant" read from
    # the other side
    for bloomDay, m, k in cases:
        answer = s.minDays(bloomDay, m, k)
        if answer != -1:
            days = sorted(set(bloomDay))
            assert days[bisect.bisect_left(days, answer)] == answer, (bloomDay, m, k)

    print("all good")
