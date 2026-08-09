class Solution:
    def maxPower(self, stations, r, k):
        # 2772 fixed the window width and found that the operation multiset
        # stopped being a choice. the leftmost position still owing something
        # could be served by exactly one window, so induction pinned every
        # count and the only question left was whether the forced answer was
        # legal. this problem fixes the width too - every station covers
        # exactly 2r+1 cities - and the choice comes back.
        #
        # what changed is the target. 2772 wanted the array to land on zero
        # exactly, so a window opened at i had to start at i: anything further
        # left would overshoot a position already settled, and overshoot was
        # fatal because operations only subtract. here the target is `power[i]
        # >= x`, an inequality, so overshoot costs nothing. a station covering
        # city i may sit anywhere in [i-r, i+r] and the cities left of i that
        # it also covers are already satisfied and cannot be harmed.
        #
        # so the argument stops being forcing and becomes an exchange. every
        # legal placement serving i covers i; the one at the far right covers
        # the longest suffix of what is still ahead; nothing behind i can
        # object. push right and no solution is lost. that is a strictly weaker
        # kind of claim than 2772's - there the multiset was unique, here many
        # placements are optimal and the greedy just names one.
        #
        # the rightmost legal city is min(i + r, n - 1) and the clamp is not a
        # boundary patch, it is the statement that stations live in cities. it
        # still covers i: i + r >= n means i > n - 1 - r, so city n-1 is within
        # r of i anyway.
        #
        # and the outer question is a maximin, which is not something the sweep
        # can answer directly. binary search converts it: "can every city reach
        # x on a budget of k" is monotone in x, and that predicate is the sweep
        # above. so the shape here is one layer taller than everything else
        # this week - the difference array is not the algorithm anymore, it is
        # the feasibility oracle inside one.
        base = self._basePower(stations, r)

        low, high = min(base), sum(stations) + k
        while low < high:
            mid = (low + high + 1) // 2
            if self._reachable(base, r, k, mid):
                low = mid
            else:
                high = mid - 1

        return low

    def _reachable(self, base, r, k, target):
        """Can every city reach `target` power by building at most `k` stations?

        The sweep from every other problem this week, with `running` holding the
        power contributed by stations built during this pass and `expiring[i]`
        removing them as their windows close.

        The only asymmetry worth noting against 2772: there were two ways to
        fail, `remaining < 0` and the window running off the end. Neither exists
        here. Overshoot is free because the target is a lower bound, and a
        deficient city always has a legal placement since the clamp guarantees
        one. The single failure mode is running out of budget, which is why the
        check reads as a running total against `k` and nothing else.
        """
        n = len(base)
        expiring = [0] * (n + 1)
        running = 0
        used = 0

        for i in range(n):
            running -= expiring[i]
            current = base[i] + running
            if current >= target:
                continue

            need = target - current
            used += need
            if used > k:
                return False

            running += need
            # built at the rightmost city still covering i, so the new window
            # is [placed - r, placed + r] and stops counting one past its end.
            # ninth syntax for that boundary in a week and a half.
            closes = min(i + r, n - 1) + r + 1
            if closes < n:
                expiring[closes] += need

        return True

    def maxPowerPlacement(self, stations, r, k):
        """Return `(answer, built)` where `built[j]` is how many to build at `j`.

        Same binary search, then one more sweep at the winning target recording
        where the stations went instead of only counting them.

        Seventh day running that the summary-versus-set split has picked the
        alternate, and it lands differently again. In 2772 the set was the
        honest object because the multiset was unique and the bool was lossy on
        top of it. Here the set is *not* unique - the exchange argument only
        says rightmost is as good as anything, not that it is the only choice -
        so this returns one witness rather than the witness. Which is worth
        keeping precisely because it cannot be checked by comparing two callers'
        answers for equality. It has to be checked by replaying it, and the
        tests below do exactly that.

        The leftover budget is deliberately not spent. Any station built after
        the sweep is satisfied raises some city's power above the minimum and
        cannot raise the minimum itself, so it is invisible to the objective.
        """
        n = len(stations)
        base = self._basePower(stations, r)
        target = self.maxPower(stations, r, k)

        built = [0] * n
        expiring = [0] * (n + 1)
        running = 0

        for i in range(n):
            running -= expiring[i]
            current = base[i] + running
            if current >= target:
                continue

            need = target - current
            placed = min(i + r, n - 1)
            built[placed] += need
            running += need
            closes = placed + r + 1
            if closes < n:
                expiring[closes] += need

        return target, built

    def maxPowerLinearScan(self, stations, r, k):
        """Walk candidate targets upward one at a time instead of bisecting.

        `O(n * answer)` and unusable on the real constraints, kept because it
        separates the two ideas the primary fuses. The sweep is a feasibility
        test and nothing more; the binary search is an unrelated observation
        about the predicate being monotone. Running the targets in order makes
        the monotonicity a claim the code visibly relies on rather than one
        buried inside a bisection that would silently return garbage if it were
        false.

        Stops at the first infeasible target and returns the one before it,
        which is the same answer the primary converges on exactly when the
        predicate really is downward closed.
        """
        base = self._basePower(stations, r)
        target = min(base)

        while self._reachable(base, r, k, target + 1):
            target += 1

        return target

    def _basePower(self, stations, r):
        """Power of each city before anything new is built.

        The window is clipped at both ends rather than wrapped or padded - a
        city near the edge genuinely sees fewer stations, and that is the
        problem's arithmetic rather than a case to correct for. It is also why
        the binary search starts at `min(base)` instead of zero: the current
        minimum is always reachable on a budget of nothing.
        """
        n = len(stations)
        prefix = [0] * (n + 1)
        for i, count in enumerate(stations):
            prefix[i + 1] = prefix[i] + count
        return [
            prefix[min(n, i + r + 1)] - prefix[max(0, i - r)]
            for i in range(n)
        ]


if __name__ == "__main__":
    s = Solution()

    assert s.maxPower([1, 2, 4, 5, 0], 1, 2) == 5
    assert s.maxPower([4, 4, 4, 4], 0, 3) == 4
    assert s.maxPower([0], 0, 0) == 0
    assert s.maxPower([0], 0, 7) == 7
    assert s.maxPower([0, 0, 0], 5, 4) == 4
    assert s.maxPower([1, 0, 1], 0, 1) == 1
    assert s.maxPower([2, 4, 2], 1, 0) == 6

    cases = [
        ([1, 2, 4, 5, 0], 1, 2),
        ([4, 4, 4, 4], 0, 3),
        ([0], 0, 0),
        ([0], 0, 7),
        ([0, 0, 0], 5, 4),
        ([1, 0, 1], 0, 1),
        ([2, 4, 2], 1, 0),
        ([3, 1, 0, 0, 2], 2, 5),
        ([0, 0, 0, 0, 0, 0], 1, 9),
        ([5, 0, 0, 0, 5], 1, 4),
    ]

    # the slow scan climbs the same predicate one step at a time, so it agrees
    # with the bisection exactly when the predicate is monotone
    for stations, r, k in cases:
        assert s.maxPowerLinearScan(stations, r, k) == s.maxPower(stations, r, k), (
            stations,
            r,
            k,
        )

    # the placement is only one witness among several, so it gets replayed
    # rather than compared - build what it says and check the minimum lands
    # on the reported answer without exceeding the budget
    for stations, r, k in cases:
        answer, built = s.maxPowerPlacement(stations, r, k)
        assert sum(built) <= k, (stations, r, k)

        total = [a + b for a, b in zip(stations, built)]
        n = len(total)
        power = [
            sum(total[max(0, i - r) : min(n, i + r + 1)]) for i in range(n)
        ]
        assert min(power) >= answer, (stations, r, k, power, answer)

    # and one exhaustive check that the greedy really is optimal, by trying
    # every way of distributing the budget on small inputs
    from itertools import product

    def brute(stations, r, k):
        n = len(stations)
        best = 0
        for extra in product(range(k + 1), repeat=n):
            if sum(extra) > k:
                continue
            total = [a + b for a, b in zip(stations, extra)]
            power = [
                sum(total[max(0, i - r) : min(n, i + r + 1)]) for i in range(n)
            ]
            best = max(best, min(power))
        return best

    for stations, r, k in [
        ([1, 0, 2], 1, 3),
        ([0, 0, 0], 0, 4),
        ([2, 1], 1, 2),
        ([1, 1, 1, 1], 1, 3),
        ([0, 3, 0], 1, 2),
        ([1, 0, 0, 1], 2, 3),
    ]:
        assert s.maxPower(stations, r, k) == brute(stations, r, k), (stations, r, k)

    print("all good")
