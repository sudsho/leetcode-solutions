import itertools
import random


class Solution:
    def maxRunTime(self, n, batteries):
        # tenth on the monotone-predicate-plus-bisect shape, first hard one in a
        # while, and the first where the predicate is a formula that only proves
        # half of what it needs to.
        #
        # the formula is a work count. over a run of t minutes the n computers
        # consume n * t battery-minutes, and a battery of capacity b can supply
        # min(b, t) of them - min, not b, because a battery cannot power two
        # computers at the same instant, so it cannot give more than t no matter
        # how large it is. so feasibility needs sum(min(b, t)) >= n * t.
        #
        # that argument is *necessity* and nothing else. it says a run of t
        # minutes cannot happen without enough work available. it does not say the
        # work can be delivered where it is needed, and every one of the previous
        # nine predicates gave me both halves in one breath because every one of
        # them was a greedy that built the thing it was testing for. see
        # maxRunTimeSchedule for the other half, which needs its own argument and
        # is the first construction in the run that the predicate does not hand me.
        if n <= 0:
            return 0

        total = sum(batteries)

        # bounds, sixth day running, and this pair is genuinely free, which after
        # the last two days i am going to state carefully rather than not at all.
        #
        # bottom: t = 0 needs 0 work. always true, and unlike 1482 it is true by
        # arithmetic rather than by a promise in the statement.
        #
        # top: sum(min(b, t)) <= total for every t, so feasibility forces
        # n * t <= total, so t <= total // n. this one does not go through a count
        # of anything, which is what went wrong yesterday - i had propped up a
        # correct bound with a sentence about how many items the extreme threshold
        # admits, and that sentence was false on ties. there is no such sentence
        # available here, because the bound falls out of the predicate's own right
        # hand side. worth noticing that the bounds i got wrong were the ones i
        # argued through a side quantity.
        low, high = 0, total // n

        # maximization, so the true half keeps mid and mid rounds *up*. fourth
        # maximization in ten, fifth day running writing the rule out.
        while low < high:
            mid = (low + high + 1) // 2
            if self._enough_work(n, batteries, mid):
                low = mid
            else:
                high = mid - 1

        return low

    def _enough_work(self, n, batteries, minutes):
        """Is there enough battery-minutes for `n` computers to run `minutes`?

        `sum(min(b, minutes)) >= n * minutes`. The cap at `minutes` is the whole
        content: a battery cannot power two computers simultaneously, so however
        large it is it contributes at most `minutes` to a run of that length.

        Monotone in the right direction, and the argument is not the usual one.
        For the previous nine I read monotonicity off a greedy - more budget, more
        room, the scan takes at least as many. Here both sides move. The left side
        `sum(min(b, t))` is non-decreasing in `t` and the right side `n * t` is
        increasing, so nothing is settled by inspection. What settles it is that
        the left side grows by at most `#{b >= t}` per unit step and that count is
        at most `len(batteries)`, while... no. That is not it either, and I wrote
        it out before noticing.

        The clean statement is about the difference. Write `g(t) = sum(min(b, t))
        - n * t`. Each `min(b, t)` is concave in `t`, `-n * t` is linear, so `g` is
        concave, and `g(0) = 0`. A concave function starting at zero is
        non-negative on an interval containing 0 and negative outside it, so
        `{t : g(t) >= 0}` is a prefix. That is the monotonicity, and it comes from
        concavity rather than from any exchange argument.

        First predicate in the run whose monotonicity proof does not mention a
        greedy at all. It is also the first one I got wrong twice on the way to
        stating it, which I am leaving in the docstring rather than tidying away,
        because both wrong versions were about counting items and the right one is
        not, and that is the same mistake as yesterday's bound.

        `O(len(batteries))` and no allocation.
        """
        available = 0
        needed = n * minutes

        for capacity in batteries:
            available += capacity if capacity < minutes else minutes
            if available >= needed:
                return True

        return available >= needed

    def maxRunTimeDirect(self, n, batteries):
        """The answer without a search: peel off the batteries that outlast the average.

        Sort descending. If the largest battery holds more than the running average
        `total / n`, then no schedule can spend all of it - the computer it feeds
        can only take `t` minutes of it and `t` is at most the average - so it is
        dedicated to one computer, the surplus is unreachable, and the problem
        drops to `n - 1` computers with that battery removed. Otherwise every
        battery is at or below the average, nothing is stranded, and the answer is
        `floor(total / n)`.

        **This is the thing the last ten days have no slot for.** The framework I
        have been building says: the search space is generically bigger than the
        answer set, and the move available to you depends on the answer set's size
        against the cost of the search it would replace. Both branches of that are
        searches. This is neither. The answer set here is `{S_k / (n - k)}` for the
        `k` peeled batteries, `n` candidates, and I do not search it - the sorted
        scan *identifies* which candidate is the answer, in one pass, with zero
        predicate calls.

        So "enumerable" was the wrong axis all along, or at least not the only one.
        The question is not how big the answer set is, it is whether membership in
        it is decidable locally. Here it is: battery `i` is peeled iff it exceeds
        the average of what remains, which is a test on one element and a running
        sum. That is what makes the scan possible and it is a property no amount of
        counting the candidates would have revealed.

        `O(m log m)` for the sort, then one pass. Strictly better than the primary,
        which costs `O(m log(total / n))`, and still second in the file for 1482's
        reason - the primary is the shape I am practising.
        """
        if n <= 0:
            return 0

        ordered = sorted(batteries, reverse=True)
        total = sum(ordered)

        for i in range(n):
            # `ordered[i] * (n - i) > total` is `ordered[i] > total / (n - i)` with
            # no float in it. worth the awkwardness: `total` reaches 1e14 here and
            # the comparison decides a branch, so a double's 53 bits are enough
            # today and are the kind of thing that stops being enough silently.
            if ordered[i] * (n - i) > total:
                total -= ordered[i]
            else:
                return total // (n - i)

        # unreachable. at `i == n - 1` the test is `ordered[n-1] > total`, and
        # `total` at that point still includes `ordered[n-1]` along with every
        # battery past index `n - 1`, of which there are `len(batteries) - n >= 0`.
        # so the test is false and the loop returns. raising rather than falling
        # through to a bare `return`, for 1482's reason: a second implementation
        # that quietly returns the wrong thing is worse than no second
        # implementation.
        raise AssertionError("peel loop ran past n-1 without settling")

    def maxRunTimeByCandidates(self, n, batteries):
        """Same answer, searched over the `n` candidate values instead of the range.

        Sort descending, let `S_k` be the sum of everything except the `k` largest.
        Rearranging the predicate at a `t` with exactly `k` batteries at or above
        it gives `t <= S_k / (n - k)`, so every feasible `t` is bounded by one of
        these `n` ratios and the answer is the largest floor among them that the
        predicate accepts. Attained and enumerable, same as 2616, and by an
        argument rather than by luck.

        **And it loses, for the tenth time in ten.** `n` is up to `1e5`. The range
        is `total / n` with `total` up to `1e14`, so bisecting it costs at most 47
        predicate calls. Building the candidates costs a sort and then searching
        them costs another `log n`, and the sort is the same sort `maxRunTimeDirect`
        does for free on its way to not searching at all.

        Which is the answer to the question I left open on the 20th, and it is a
        negative one. I wanted a problem in this shape where the answer set is
        cheaper *by an exponent* rather than by a constant, on the grounds that ten
        problems all lopsided in the same direction means I have only seen one side
        of the rule. There is no such problem here and there cannot be. The range
        is always some quantity built out of the input's numbers, so its logarithm
        is bounded by the width of a machine integer - 30 to 60, always, in every
        problem of this shape I will ever open. The answer set is always indexed by
        the input, so its size is `n`, which the constraints let run to `1e5` and
        up. `log(range)` is capped by the *format* and `|answer set|` is not.

        So the lopsidedness is not a property of the ten problems I happened to
        pick. It is forced, and I spent ten days building a comparison whose result
        was decided before I started. That is the third night running that
        something I was treating as a property of the problem turned out to be
        relative to something outside it - the representation on the 19th, the
        alternative on the 20th, the constraint format tonight - except this one is
        worse than the other two, because the outside thing is not part of the
        mathematics at all. It is an artefact of the venue.

        `O(m log m)` to sort, `O(m log n)` to search. Kept because the agreement
        with the primary is a real test of the attainment claim.
        """
        if n <= 0:
            return 0

        ordered = sorted(batteries, reverse=True)
        suffix = sum(ordered)

        candidates = [0]
        for k in range(n):
            candidates.append(suffix // (n - k))
            suffix -= ordered[k]

        candidates = sorted(set(candidates))

        low, high = 0, len(candidates) - 1
        while low < high:
            mid = (low + high + 1) // 2
            if self._enough_work(n, batteries, candidates[mid]):
                low = mid
            else:
                high = mid - 1

        return candidates[low]

    def maxRunTimeSchedule(self, n, batteries):
        """Return `(minutes, plan)` - the answer and a schedule that realises it.

        `plan` holds `(battery, computer, start, end)` with times in `[0, minutes]`.
        Every computer's intervals tile `[0, minutes]` exactly, and no battery
        appears in two overlapping intervals.

        Sixteenth day of the summary-versus-set split, and the first where the
        witness is not a by-product of the predicate.

        The nine before this all had a greedy inside the predicate, so the object
        proving feasibility was already built by the time the predicate returned
        true and the witness was a matter of writing it down. Here the predicate is
        a work count and it proves only that a run of `t` minutes is not ruled out
        by the total supply. Sufficiency is a separate claim with a separate
        argument, and it is this:

        Lay the batteries end to end on one timeline of length `n * t`, each
        contributing `min(b, t)`. Cut the timeline into `n` pieces of length `t`
        and read piece `j` as computer `j`'s minute-by-minute schedule. A battery
        that straddles a cut runs computer `j` over `[a, t]` and computer `j + 1`
        over `[0, x]`, and those overlap in wall clock unless `x <= a`. They do not
        overlap, because `x = min(b, t) - (t - a) <= t - (t - a) = a`. **The cap at
        `t` is what makes the construction legal, and it is the same cap that made
        the count correct.** One inequality doing both jobs, which is why I read
        the predicate as complete on the first pass.

        Non-canonical, and this time for symmetry with nothing else mixed in.
        Permuting the computers is a symmetry of the entire problem - they are
        interchangeable by definition, not by a coincidence in the input - so the
        `n!` relabelings of any schedule are all equally good and no argument picks
        one. That is 2528's tied cities in a purer form.

        Which lines up against yesterday exactly. Yesterday was slack with no
        symmetry available and the leftmost rule still named a member. Today is
        symmetry that no rule can break, on a problem where there is slack too -
        the battery order is free as well. Two days, the two halves separated in
        both directions, and on the 17th I had them confounded. The pair is the
        test I said on the 20th I had only seen one side of, and I got it a day
        later on a different thread than the one I was asking about.

        `O(m + n)` intervals after the primary.
        """
        minutes = self.maxRunTime(n, batteries)
        if minutes == 0:
            return 0, []

        plan = []
        cursor = 0
        horizon = n * minutes

        for index, capacity in enumerate(batteries):
            if cursor >= horizon:
                break

            remaining = min(capacity, minutes, horizon - cursor)
            while remaining > 0:
                computer, start = divmod(cursor, minutes)
                chunk = min(remaining, minutes - start)
                plan.append((index, computer, start, start + chunk))
                cursor += chunk
                remaining -= chunk

        # unreachable when the predicate is right, and that is exactly why it is
        # checked. the predicate says the supply covers the horizon; this loop is
        # the only thing that says the supply can be *placed*. if they ever
        # disagree the answer is still returned and nothing downstream notices,
        # which is 1482's silent failure with a different cause.
        if cursor != horizon:
            raise AssertionError("feasible run time did not fill the schedule")

        return minutes, plan

    def maxRunTimeSingle(self, n, batteries):
        """Shortcut for `n == 1`: the answer is the total.

        One computer, no simultaneity, so every battery-minute is reachable and
        nothing is stranded. Same role as 2517's `k == 2` and 2616's `p == 1` - the
        input where the algorithm makes no decision, which makes it the cleanest
        thing to check the general path against. It is also the input that pushes
        the range to its ceiling, which random cases essentially never do.

        Returns `None` when it does not apply.
        """
        if n != 1:
            return None

        return sum(batteries)


if __name__ == "__main__":
    s = Solution()

    assert s.maxRunTime(2, [3, 3, 3]) == 4
    assert s.maxRunTime(2, [1, 1, 1, 1]) == 2
    assert s.maxRunTime(3, [10, 10, 3, 5]) == 8
    assert s.maxRunTime(1, [7]) == 7
    assert s.maxRunTime(2, [1, 1]) == 1

    cases = [
        (2, [3, 3, 3]),
        (2, [1, 1, 1, 1]),
        (3, [10, 10, 3, 5]),
        (1, [7]),
        (2, [1, 1]),
        (1, [1, 2, 3, 4, 5]),
        (3, [1, 1, 1]),
        (2, [100, 1, 1]),
        (2, [100, 100]),
        (4, [5, 5, 5, 5, 20]),
        (3, [2, 2, 2, 2, 2, 2]),
        (5, [1, 1, 1, 1, 1]),
        (2, [1000000000, 1]),
        (3, [7, 7, 7, 1]),
        (4, [9, 3, 3, 3, 3, 3]),
        (2, [6, 6, 6, 6]),
    ]

    for n, batteries in cases:
        assert 1 <= n <= len(batteries), (n, batteries)
        assert all(b >= 1 for b in batteries), batteries

    # the two ends of the range, checked rather than asserted in prose. sixth day
    # of writing a bounds paragraph and the second of turning it into asserts,
    # after yesterday's top bound came out correct for a reason that was false on
    # ties.
    #
    # and the assert caught something, though a smaller thing than yesterday. i
    # first wrote the top line as `_enough_work(n, batteries, total // n)`, on the
    # assumption that the top of the range is feasible, which it was on all nine
    # previous days - there the extreme threshold was always an achievable
    # configuration. it is not here. [100, 1, 1] with n = 2 has total // n = 51
    # and only 53 reachable battery-minutes against the 102 that would need. the
    # bound is an upper bound and nothing more, because it comes from dropping the
    # min() rather than from exhibiting anything. so the top end gets tested as a
    # bound - the point above it fails - and not as a point.
    for n, batteries in cases:
        assert s._enough_work(n, batteries, 0)
        assert not s._enough_work(n, batteries, sum(batteries) // n + 1)
        assert s.maxRunTime(n, batteries) <= sum(batteries) // n

    # the predicate against its own definition, computed the slow obvious way.
    # a predicate that is wrong but still monotone hands back a confident wrong
    # boundary and nothing downstream notices.
    def enough_work_brute(n, batteries, minutes):
        return sum(min(b, minutes) for b in batteries) >= n * minutes

    # sampled rather than swept, and the sampling is not laziness: [1000000000, 1]
    # with n = 1 has a range of a billion and the sweep i wrote first sat there
    # for two minutes before i killed it. the window that matters is the one
    # around the boundary, so take the first 200 thresholds, the last 200, and 200
    # either side of the answer.
    def thresholds(n, batteries):
        span = sum(batteries) // n + 3
        answer = s.maxRunTime(n, batteries)
        window = set(range(0, min(200, span)))
        window |= set(range(max(0, span - 200), span))
        window |= set(range(max(0, answer - 200), min(span, answer + 200)))
        return sorted(window)

    for n, batteries in cases:
        for minutes in thresholds(n, batteries):
            assert s._enough_work(n, batteries, minutes) == enough_work_brute(
                n, batteries, minutes
            ), (n, batteries, minutes)

    # monotonicity, in the direction the bisect uses. this is the concavity claim
    # from the docstring, checked rather than trusted, because it is the first
    # monotonicity in the run that does not come from a greedy and I had two wrong
    # arguments for it before the right one.
    for n, batteries in cases:
        flags = [s._enough_work(n, batteries, t) for t in thresholds(n, batteries)]
        assert all(a >= b for a, b in zip(flags, flags[1:])), (n, batteries)

    # necessity and sufficiency, separately, which is the whole of today's note.
    # necessity: t + 1 fails the work count, and the work count is an upper bound
    # on what any schedule could deliver, so no schedule exists. sufficiency: the
    # schedule at t is built and validated below. together those pin the answer
    # exactly, with no brute force anywhere - and the run has not had that before,
    # because the nine before this proved both halves in one greedy.
    for n, batteries in cases:
        minutes = s.maxRunTime(n, batteries)
        assert not enough_work_brute(n, batteries, minutes + 1), (n, batteries)

    # the schedule is real. every computer's intervals tile [0, t] with no gap and
    # no overlap, no battery is asked to be in two places at once, and no battery
    # gives more than it holds.
    for n, batteries in cases:
        minutes, plan = s.maxRunTimeSchedule(n, batteries)

        per_computer = {}
        per_battery = {}
        for battery, computer, start, end in plan:
            assert 0 <= start < end <= minutes, (battery, computer, start, end)
            per_computer.setdefault(computer, []).append((start, end))
            per_battery.setdefault(battery, []).append((start, end))

        assert sorted(per_computer) == list(range(n)), (n, batteries)

        for computer, intervals in per_computer.items():
            intervals.sort()
            assert intervals[0][0] == 0, (n, batteries, computer)
            assert intervals[-1][1] == minutes, (n, batteries, computer)
            for (_, end), (start, _) in zip(intervals, intervals[1:]):
                assert end == start, (n, batteries, computer, intervals)

        for battery, intervals in per_battery.items():
            intervals.sort()
            for (_, end), (start, _) in zip(intervals, intervals[1:]):
                assert end <= start, (n, batteries, battery, intervals)
            used = sum(end - start for start, end in intervals)
            assert used <= batteries[battery], (n, batteries, battery, used)
            assert used <= minutes, (n, batteries, battery, used)

    # the peeling scan agrees with the search. it shares nothing with the primary -
    # no predicate call, no bisect - so agreement is a real cross-check and not a
    # restatement.
    for n, batteries in cases:
        assert s.maxRunTimeDirect(n, batteries) == s.maxRunTime(n, batteries), (
            n,
            batteries,
        )

    # and the candidate-space search agrees too, which is what tests the attainment
    # claim: the answer really is one of the n ratios S_k / (n - k).
    for n, batteries in cases:
        assert s.maxRunTimeByCandidates(n, batteries) == s.maxRunTime(n, batteries), (
            n,
            batteries,
        )

    # attainment stated directly as well, since the agreement above would survive
    # both implementations being wrong the same way.
    for n, batteries in cases:
        answer = s.maxRunTime(n, batteries)
        ordered = sorted(batteries, reverse=True)
        suffix = sum(ordered)
        ratios = set()
        for k in range(n):
            ratios.add(suffix // (n - k))
            suffix -= ordered[k]
        assert answer in ratios, (n, batteries, answer, sorted(ratios))

    # n == 1 removes the simultaneity constraint and therefore the whole problem,
    # so the general path has to agree with the sum.
    for _, batteries in cases:
        assert s.maxRunTime(1, batteries) == s.maxRunTimeSingle(1, batteries), batteries

    assert s.maxRunTimeSingle(2, [1, 2]) is None

    # every n from 1 up to len(batteries) on the same array, so the boundary is
    # walked across rather than sampled. more computers can never run longer, which
    # is monotonicity of the problem in n rather than of the predicate in t - a
    # different claim, and nothing else here would catch it failing.
    for _, batteries in cases:
        previous = None
        for n in range(1, len(batteries) + 1):
            answer = s.maxRunTime(n, batteries)
            if previous is not None:
                assert answer <= previous, (batteries, n, answer, previous)
            assert s.maxRunTimeDirect(n, batteries) == answer, (batteries, n)
            previous = answer

    # the one input where a schedule genuinely has to strand something. a battery
    # bigger than the run time cannot spend its surplus, and the peel is the step
    # that notices. asserted directly because the property checks above would all
    # pass on an implementation that silently counted the surplus as usable.
    assert s.maxRunTime(2, [100, 1, 1]) == 2
    assert s.maxRunTimeDirect(2, [100, 1, 1]) == 2
    _, stranded_plan = s.maxRunTimeSchedule(2, [100, 1, 1])
    assert sum(end - start for i, _, start, end in stranded_plan if i == 0) == 2

    # brute force over explicit assignments on the small cases. this is the only
    # check that does not go through the work count at all - it asks whether some
    # partition of the batteries into n groups leaves every group summing to at
    # least t, which is a *sufficient* condition weaker than the real one (it
    # forbids splitting a battery across computers) and therefore a lower bound.
    # the answer must be at least what it finds.
    def best_without_splitting(n, batteries, ceiling):
        best = 0
        for assignment in itertools.product(range(n), repeat=len(batteries)):
            loads = [0] * n
            for battery, computer in zip(batteries, assignment):
                loads[computer] += battery
            best = max(best, min(loads))
        return min(best, ceiling)

    for n, batteries in cases:
        if len(batteries) > 6 or n > 3:
            continue
        answer = s.maxRunTime(n, batteries)
        assert answer >= best_without_splitting(n, batteries, answer + 10 ** 9), (
            n,
            batteries,
            answer,
        )

    # random cases across all three implementations. the fixed cases are all
    # hand-picked for a reason and hand-picked cases stop finding things once they
    # pass once.
    rng = random.Random(2141)
    for _ in range(500):
        m = rng.randint(1, 9)
        n = rng.randint(1, m)
        batteries = [rng.randint(1, 30) for _ in range(m)]

        answer = s.maxRunTime(n, batteries)
        assert s.maxRunTimeDirect(n, batteries) == answer, (n, batteries)
        assert s.maxRunTimeByCandidates(n, batteries) == answer, (n, batteries)
        assert not enough_work_brute(n, batteries, answer + 1), (n, batteries)

        minutes, plan = s.maxRunTimeSchedule(n, batteries)
        assert minutes == answer
        loads = [0] * n
        for _, computer, start, end in plan:
            loads[computer] += end - start
        assert loads == [answer] * n, (n, batteries, loads)

    # and a large one, because the whole argument in today's note is about what
    # happens at the constraint ceiling and every case above is small enough that
    # the range search and the candidate search cost the same.
    big = [rng.randint(1, 10 ** 9) for _ in range(2000)]
    for n in (1, 2, 17, 500, 2000):
        answer = s.maxRunTime(n, big)
        assert s.maxRunTimeDirect(n, big) == answer, n
        assert s.maxRunTimeByCandidates(n, big) == answer, n

    print("all good")
