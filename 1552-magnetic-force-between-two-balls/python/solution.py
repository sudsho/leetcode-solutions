class Solution:
    def maxDistance(self, position, m):
        # yesterday's problem was a maximin that the sweep could not answer
        # directly, so binary search turned it into a feasibility question and
        # the sweep became the oracle inside one. same shape here: maximize the
        # minimum gap, bisect on the gap, and the predicate "can m balls sit at
        # these positions with every pair at least `gap` apart" is a single
        # left-to-right pass.
        #
        # what is different is the direction the greedy pushes, and that turns
        # out to be the whole content of the problem.
        #
        # 2528 pushed right. a station serving city i could sit anywhere in
        # [i-r, i+r], and the rightmost choice covered the longest suffix of
        # what was still ahead. the thing extending forward was coverage - a
        # benefit - so extending it as far as possible was free.
        #
        # here the greedy pulls left. a ball goes at the earliest position that
        # clears the last one, because the thing extending forward is the
        # occupied prefix, and that is a cost. every unit of line spent behind
        # is a unit the remaining balls cannot use.
        #
        # so the two are the same exchange argument and not opposite ones:
        # leave the most freedom for what has not been decided yet. the
        # direction only flips because the quantity being pushed forward
        # changes sign. that is worth writing down because the direction is the
        # part i would otherwise memorize per problem.
        #
        # one real asymmetry though. in 2528 rightmost was forced - pulling
        # left genuinely loses solutions, because a station left of i covers
        # less of what is ahead and there is no compensating gain. here the
        # mirror is legal. reflect the line and the rightmost-anchored greedy
        # is just as correct, because distance is symmetric and nothing in the
        # objective distinguishes the ends. `maxDistanceMirrored` below is that
        # claim as executable code rather than a remark.
        spots = sorted(position)

        # sorting is not bookkeeping here. 2528 handed me the geometry already
        # in index order - city i was at index i - so "further right" was a
        # fact about the array. this input is an unordered set of coordinates
        # and "as early as possible" means nothing until the order exists.
        low, high = 1, (spots[-1] - spots[0]) // (m - 1)

        # the upper bound is pigeonhole: m balls inside a span of W leave m-1
        # gaps summing to at most W, so the smallest is at most W // (m-1).
        # it is also why the range is never empty - the positions are distinct
        # integers, so the span is at least n-1 >= m-1 and `high` is at least
        # 1. no guard needed for low > high, which is the kind of thing i have
        # been patching after the fact all week.
        while low < high:
            mid = (low + high + 1) // 2
            if self._placeable(spots, m, mid):
                low = mid
            else:
                high = mid - 1

        return low

    def _placeable(self, spots, m, gap):
        """Can `m` balls sit in `spots` with consecutive ones at least `gap` apart?

        Anchor at `spots[0]`, then take every position that clears the last ball
        taken. Two separate exchange claims, and they are easy to run together
        by accident.

        The anchor: some optimal arrangement uses the leftmost position. Given
        any valid arrangement, slide its leftmost ball down to `spots[0]`. Only
        one gap changes and it only grows, so validity survives. The anchor is
        free.

        The step: given where the last ball sits, taking the earliest legal
        position is at least as good as any later one. A later choice leaves a
        shorter suffix and the remaining balls have to fit in it, so any
        arrangement built on the later choice maps onto one built on the
        earlier. Nothing behind can object, because the gap to the previous ball
        is already satisfied and pulling left would be the only way to break it.

        Only consecutive gaps are checked, which is the whole reason this is a
        linear pass and not a pairwise one. The positions are sorted, so any
        non-adjacent pair is separated by at least the sum of the gaps between
        them.
        """
        placed = 1
        last = spots[0]

        for x in spots[1:]:
            if x - last < gap:
                continue
            placed += 1
            if placed == m:
                return True
            last = x

        return placed >= m

    def maxDistancePlacement(self, position, m):
        """Return `(answer, chosen)` where `chosen` are the sorted ball positions.

        Eighth day running that the summary-versus-set split has picked the
        alternate. Yesterday the set was one witness among many and could not be
        validated by having two callers agree, so the test replayed it instead.
        Same verdict here for the same reason, but the ambiguity has a name now:
        the mirror. `maxDistanceMirrored` produces a different `chosen` on most
        inputs and is equally correct, so equality of placements is not a
        property either one has.

        What the pair does give is a real check that comparing two copies of the
        same greedy would not. The answers must match even though the witnesses
        do not, and the assertions below lean on that rather than on the
        placement itself.
        """
        spots = sorted(position)
        gap = self.maxDistance(position, m)

        chosen = [spots[0]]
        for x in spots[1:]:
            if len(chosen) == m:
                break
            if x - chosen[-1] >= gap:
                chosen.append(x)

        return gap, chosen

    def maxDistanceMirrored(self, position, m):
        """Same search, run on the line reflected through zero.

        Negating every coordinate reverses the sorted order and preserves every
        pairwise distance, so the leftmost-anchored greedy on the reflection is
        exactly the rightmost-anchored greedy on the original. It has to return
        the same answer.

        This is here because the direction was the one thing I could not
        transfer from yesterday. In 2528 the direction was forced and swapping
        it produced wrong answers - the two ends of that problem were not
        interchangeable, since coverage extended forward only. Here they are,
        and I would rather the symmetry be a test that fails loudly if I have
        misread it than a sentence in a comment.
        """
        reflected = [-x for x in position]

        spots = sorted(reflected)
        low, high = 1, (spots[-1] - spots[0]) // (m - 1)
        while low < high:
            mid = (low + high + 1) // 2
            if self._placeable(spots, m, mid):
                low = mid
            else:
                high = mid - 1

        return low

    def maxDistanceAdjacent(self, position, m):
        """Shortcut for `m == len(position)`: every position is used.

        There is no choice left, so the minimum gap is the minimum adjacent gap
        and the search has nothing to search. Kept separate rather than folded
        into the primary as an early return, because it is the one input where
        the greedy is not making a decision at all, and that makes it the
        cleanest thing to check the general path against.

        Returns `None` when the shortcut does not apply, so a caller cannot use
        it by accident on an input it says nothing about.
        """
        if m != len(position):
            return None

        spots = sorted(position)
        return min(b - a for a, b in zip(spots, spots[1:]))


if __name__ == "__main__":
    s = Solution()

    assert s.maxDistance([1, 2, 3, 4, 7], 3) == 3
    assert s.maxDistance([5, 4, 3, 2, 1, 1000000000], 2) == 999999999
    assert s.maxDistance([1, 2], 2) == 1
    assert s.maxDistance([79, 74, 57, 22], 4) == 5
    assert s.maxDistance([1, 2, 3, 4, 5, 6, 7, 8, 9], 5) == 2

    cases = [
        ([1, 2, 3, 4, 7], 3),
        ([5, 4, 3, 2, 1, 1000000000], 2),
        ([1, 2], 2),
        ([79, 74, 57, 22], 4),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], 5),
        ([0, 10, 20, 30, 40], 3),
        ([1, 8, 9, 10, 11, 20], 3),
        ([3, 1, 4, 1000, 1001], 2),
        ([0, 1, 3, 7, 15, 31], 4),
        ([100, 1, 50, 25, 75], 3),
    ]

    # the reflection is the same greedy anchored at the other end. it disagrees
    # about where the balls go and must not disagree about the gap.
    for position, m in cases:
        assert s.maxDistanceMirrored(position, m) == s.maxDistance(position, m), (
            position,
            m,
        )

    # the placement is one witness of several, so it gets replayed rather than
    # compared - take what it says, check the count and the tightest gap.
    for position, m in cases:
        gap, chosen = s.maxDistancePlacement(position, m)
        assert len(chosen) == m, (position, m, chosen)
        assert len(set(chosen)) == m, (position, m, chosen)
        assert set(chosen) <= set(position), (position, m, chosen)
        assert min(b - a for a, b in zip(chosen, chosen[1:])) >= gap, (
            position,
            m,
            chosen,
        )

    # when every position is used there is no decision to make, so the general
    # path has to agree with the plain minimum adjacent gap
    for position in [[1, 2, 3, 4, 7], [79, 74, 57, 22], [0, 1, 3, 7, 15, 31]]:
        expected = s.maxDistanceAdjacent(position, len(position))
        assert s.maxDistance(position, len(position)) == expected, position

    assert s.maxDistanceAdjacent([1, 2, 3], 2) is None

    # and the exhaustive check, which is the only one that tests the greedy
    # rather than the arithmetic around it
    from itertools import combinations

    def brute(position, m):
        spots = sorted(position)
        best = 0
        for pick in combinations(spots, m):
            gap = min(b - a for a, b in zip(pick, pick[1:]))
            best = max(best, gap)
        return best

    for position, m in [
        ([1, 2, 3, 4, 7], 3),
        ([1, 2, 3, 4, 7], 2),
        ([0, 10, 20, 30, 40], 3),
        ([1, 8, 9, 10, 11, 20], 3),
        ([0, 1, 3, 7, 15, 31], 4),
        ([100, 1, 50, 25, 75], 3),
        ([2, 3, 5, 8, 13, 21], 3),
        ([1, 4, 5, 9], 2),
    ]:
        assert s.maxDistance(position, m) == brute(position, m), (position, m)

    print("all good")
