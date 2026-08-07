class Solution:
    def checkArray(self, nums, k):
        # yesterday's problem ran the map backwards: here is the array, what is
        # the cheapest pile of range updates that builds it. this one runs it
        # backwards too, with one thing taken away - every operation is exactly
        # k wide. and removing that one freedom changes what kind of question
        # it is, which is the part worth keeping.
        #
        # in 1526 an operation could be any width, so there were many multisets
        # of operations producing the target and the question was which is
        # smallest. here there is at most one. index 0 can only be touched by
        # an operation starting at 0, so the count starting there is forced to
        # be nums[0]. now index 1's remaining demand is fixed, and only an
        # operation starting at 1 can still reach it, so that count is forced
        # too. induction all the way along.
        #
        # so there is nothing to minimize. the operation multiset is a function
        # of the input, not a choice, and the only remaining question is whether
        # the one candidate is legal. that is why the problem returns a bool.
        # calling this greedy is a slight lie - greedy implies picking well at
        # each step, and there is never a second option to pass over.
        #
        # same forced-choice argument as 995, where the only way to fix a bit
        # still reading 0 at i was to open a window at i. difference is that
        # flips compose mod 2 so that one tracked a parity; decrements compose
        # over the integers, so this tracks a running count. the shape of the
        # argument survives the change, the state does not.
        #
        # two ways the forced multiset turns out to be illegal:
        #
        #   remaining < 0 - the operations already in flight have pushed this
        #     position below zero. nothing can lift it back, since every
        #     operation only subtracts.
        #   i + k > n - the position still owes something and no k-wide window
        #     covering it fits inside the array anymore.
        #
        # `expiring` is the difference array, holding operations rather than
        # values: an operation opened at i covers [i, i+k-1] and stops counting
        # at i+k. that closing index is the half-open version, and it is pinned
        # rather than chosen - which is exactly the freedom 1526 had. there the
        # closes were free because a close could always be paired against some
        # already-open start; here the close lands k steps after its open and
        # nowhere else, so it can fall off the end and make the whole thing
        # infeasible. eighth syntax for that boundary in about a week.
        n = len(nums)
        expiring = [0] * (n + 1)
        active = 0

        for i, value in enumerate(nums):
            active -= expiring[i]
            remaining = value - active
            if remaining < 0:
                return False
            if remaining > 0:
                if i + k > n:
                    return False
                active += remaining
                expiring[i + k] = remaining

        return True

    def checkArrayOperations(self, nums, k):
        """Return the operations themselves as start-index counts, or None.

        Same sweep, but keeping `starts[i]` = how many operations begin at `i`
        instead of collapsing it into a running total. Returns None when the
        array cannot be cleared.

        This exists to make the determinism visible rather than argued. The
        list that comes back is not *a* solution, it is *the* solution - there
        is no other multiset of `k`-wide operations that zeroes the array, so
        two different callers cannot get two different answers here.

        That is the sharpest contrast with 1526 I have found. There the same
        construction routine was the achievability half of a lower-bound proof:
        the count had been established by a counting argument and the operations
        were built to show the bound was attainable. Here there is no bound and
        nothing to attain. Building the operations *is* the algorithm, and the
        primary above is that construction with the operations thrown away
        because the problem only asked whether it survived to the end.

        Sixth day running that the summary-versus-set distinction picks the
        alternate, and it lands the other way round this time. On the previous
        five the summary was sufficient and the set was kept for a hypothetical
        follow-up. Here the set is what the computation actually produces and
        the bool is the lossy thing.
        """
        n = len(nums)
        starts = [0] * n
        expiring = [0] * (n + 1)
        active = 0

        for i, value in enumerate(nums):
            active -= expiring[i]
            remaining = value - active
            if remaining < 0:
                return None
            if remaining > 0:
                if i + k > n:
                    return None
                starts[i] = remaining
                active += remaining
                expiring[i + k] = remaining

        return starts

    def checkArraySimple(self, nums, k):
        """Subtract from a working copy directly, no difference array.

        Walk every position that could start an operation, and if it is still
        nonzero apply that many operations there by subtracting across the whole
        window. Whatever is left at the end must already be zero.

        `O(n*k)` and too slow on the real constraints, kept because it states the
        forced recurrence with nothing standing in front of it. The primary's
        `active` counter is precisely this loop's inner subtraction, deferred:
        both compute the same `remaining` at every index, one by having already
        paid for it and one by paying at the moment the value is read.

        Also the version that makes the tail condition obvious. The loop stops
        at `n - k`, so the final `k - 1` positions never get an operation of
        their own and have to arrive at zero as a side effect of earlier
        windows. The primary reports that same fact as `i + k > n`, which is
        the same statement made one index at a time.

        Handles `k > n` without a special case: the range is empty, nothing is
        applied, and the answer is whether the input was already all zeros.
        """
        work = list(nums)
        n = len(work)

        for i in range(n - k + 1):
            if work[i] < 0:
                return False
            amount = work[i]
            if amount:
                for j in range(i, i + k):
                    work[j] -= amount

        return all(value == 0 for value in work)


if __name__ == "__main__":
    s = Solution()

    assert s.checkArray([2, 2, 3, 1, 1, 0], 3) is True
    assert s.checkArray([1, 3, 1, 1], 2) is False
    assert s.checkArray([0, 0, 0], 2) is True
    assert s.checkArray([5], 1) is True
    assert s.checkArray([1, 1], 3) is False
    assert s.checkArray([0, 0], 3) is True
    assert s.checkArray([4, 4, 4, 4], 4) is True
    assert s.checkArray([1, 2, 1], 3) is False

    # the operations are unique, so the reconstruction agrees with the bool
    # everywhere rather than merely on the cases that pass
    cases = [
        ([2, 2, 3, 1, 1, 0], 3),
        ([1, 3, 1, 1], 2),
        ([0, 0, 0], 2),
        ([5], 1),
        ([1, 1], 3),
        ([0, 0], 3),
        ([4, 4, 4, 4], 4),
        ([1, 2, 1], 3),
        ([3, 3, 3, 3, 3], 2),
    ]
    for nums, k in cases:
        expected = s.checkArray(nums, k)
        assert s.checkArraySimple(nums, k) is expected, (nums, k)
        assert (s.checkArrayOperations(nums, k) is not None) is expected, (nums, k)

    # and when they exist, applying them really does clear the array
    for nums, k in cases:
        starts = s.checkArrayOperations(nums, k)
        if starts is None:
            continue
        work = list(nums)
        for i, count in enumerate(starts):
            if not count:
                continue
            for j in range(i, i + k):
                work[j] -= count
        assert all(value == 0 for value in work), (nums, k)

    print("all good")
