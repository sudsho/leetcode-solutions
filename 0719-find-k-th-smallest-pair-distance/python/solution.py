import bisect
import heapq


class Solution:
    def smallestDistancePair(self, nums, k):
        # fourth day on this outer loop. yesterday's conclusion was that the
        # shape is exactly two things - a monotone predicate and a bisect that
        # finds its boundary - and everything else is whatever answering the
        # predicate takes. picked this to test that, because the predicate here
        # is not a feasibility question at all. it counts.
        #
        # and counting changes what the boundary means, which is the whole day.
        #
        # the last three problems all asked for the smallest x that can be done.
        # "can be done" was the question, so the answer being achievable was
        # baked into what was being asked and never needed an argument. this
        # asks for the k-th smallest distance that actually occurs between two
        # elements. that is a different kind of object - it is an order
        # statistic of a multiset i am never going to build, since there are
        # n(n-1)/2 of its elements.
        #
        # the bridge is one line and it is worth writing out rather than
        # trusting. let c(x) = #{pairs with distance <= x}. the k-th smallest
        # distance is by definition the smallest x with c(x) >= k, because
        # c is the cdf of the multiset and the k-th order statistic is where
        # the cdf first reaches k. so bisecting on c(x) >= k over the integer
        # range [0, max - min] returns the right number.
        #
        # but the range i bisect over is every integer in [0, max - min], and
        # most of those are not distances between any two elements. so the
        # boundary could a priori land on a value nothing realizes. it can't,
        # and here is why: if x is minimal with c(x) >= k then c(x - 1) < k, so
        # c(x) > c(x - 1), so some pair has distance exactly x. the search space
        # being wrong is repaired for free by the boundary being a jump in c.
        # that is the first time in four days the answer needed an attainment
        # argument, and it is the first time the searched set was bigger than
        # the set of possible answers.
        nums = sorted(nums)

        # 0 is always a legal low even when no pair is at distance 0 - it just
        # fails the predicate and the search moves off it. the high end is the
        # full spread, which is the largest distance in the multiset, so
        # c(high) is n(n-1)/2 >= k and the range is nonempty. third day running
        # that the bound is read off the structure and needs no guard.
        low, high = 0, nums[-1] - nums[0]

        while low < high:
            mid = (low + high) // 2
            if self._count_within(nums, mid) >= k:
                high = mid
            else:
                low = mid + 1

        return low

    def _count_within(self, nums, limit):
        """How many pairs of `nums` (sorted) are within `limit` of each other?

        Two-pointer sweep: for each right end, walk `left` forward until the
        window fits, then every index in `[left, right)` pairs with `right`, so
        the window contributes `right - left`.

        There are two separate monotonicity claims stacked here and running
        them together cost me the first version of this.

        The outer one is the one the bisect needs: `c` is non-decreasing in
        `limit`, since widening the limit can only admit pairs. That is what
        makes the predicate `c >= k` upward closed.

        The inner one is what makes this pass linear rather than quadratic:
        `left` never moves backwards as `right` advances. If `left` is the
        smallest index with `nums[right] - nums[left] <= limit`, then for
        `right + 1` the array value only grew, so the smallest legal index only
        grew too. Nothing about the bisect depends on this - it is a fact about
        the sorted order, and it would still hold if the predicate were being
        asked once.

        They are different claims about different variables and neither implies
        the other. I had been reading "monotone" as a single property of the
        setup for three days.
        """
        count = 0
        left = 0

        for right, value in enumerate(nums):
            while value - nums[left] > limit:
                left += 1
            count += right - left

        return count

    def smallestDistancePairWitness(self, nums, k):
        """Return `(distance, (a, b))` where `b - a` is the k-th smallest distance.

        Tenth day of the summary-versus-set split, and the witness is
        non-canonical for the third distinct reason in four days. 1552's was
        symmetry - a mirrored placement was equally good. 2064's was slack -
        a spare store could go somewhere that was not the bottleneck. This one
        is multiplicity, and it is a stronger kind of non-canonical than
        either: the answer *is* a value, and every pair separated by that value
        realizes it equally. There is no sense in which one of them is the
        witness. The other two at least had a canonical choice available if I
        had wanted to define one.

        So this returns some pair, found by scanning for the first index whose
        partner exists, and the tests check the property rather than the pair.

        The scan works because attainment is already proved - `bisect_left` on
        `nums[j] - ans` finds where the partner would be, and equality there is
        the check that it is present. Some `j` must succeed.
        """
        nums = sorted(nums)
        ans = self.smallestDistancePair(nums, k)

        for j, high in enumerate(nums):
            i = bisect.bisect_left(nums, high - ans, 0, j)
            if i < j and high - nums[i] == ans:
                return ans, (nums[i], high)

        # unreachable - the boundary of a counting predicate is a jump, so the
        # distance occurs. raising rather than returning None because this
        # failing would mean the attainment argument above is wrong, which is
        # not a case to handle quietly.
        raise AssertionError("k-th distance not realized by any pair")

    def smallestDistancePairHeap(self, nums, k):
        """Same answer by merging n sorted lists and popping k times.

        For a fixed left index `i`, the distances `nums[j] - nums[i]` for
        `j > i` are already sorted ascending. So the whole multiset of distances
        is `n - 1` sorted lists, and the k-th smallest is a k-way merge: seed
        the heap with each list's head `(i, i + 1)` and pop k times, pushing the
        successor `(i, j + 1)` after each pop.

        Kept for the reason the heap alternate was kept yesterday, and it holds
        up better here. This shares nothing with the bisect - no counting, no
        predicate, no monotonicity in the limit, and crucially no two-pointer
        sweep, which is the part of the primary I am least sure of by
        inspection. When they agree, the sweep counted correctly.

        `O(n + k log n)`, which is fine for the small `k` the tests use and
        hopeless for the `k` near `n^2` the constraints permit. That is the
        honest reason it is an alternate and not the answer.
        """
        nums = sorted(nums)
        heap = [(nums[i + 1] - nums[i], i, i + 1) for i in range(len(nums) - 1)]
        heapq.heapify(heap)

        for _ in range(k - 1):
            _, i, j = heapq.heappop(heap)
            if j + 1 < len(nums):
                heapq.heappush(heap, (nums[j + 1] - nums[i], i, j + 1))

        return heap[0][0]

    def smallestDistancePairMinGap(self, nums, k):
        """Shortcut for `k == 1`: the smallest distance is the smallest adjacent gap.

        No search. The closest pair in a sorted array is adjacent, since any
        non-adjacent pair straddles an adjacent one whose gap is no larger.

        Same role as yesterday's saturated case - the one input where the
        algorithm makes no decision, which makes it the cleanest thing to check
        the general path against. It also pins down the `low = 0` end of the
        range, which is the end I would otherwise never exercise.

        Returns `None` when the shortcut does not apply, so it cannot be used by
        accident on an input it says nothing about.
        """
        if k != 1:
            return None

        nums = sorted(nums)

        return min(b - a for a, b in zip(nums, nums[1:]))


if __name__ == "__main__":
    s = Solution()

    assert s.smallestDistancePair([1, 3, 1], 1) == 0
    assert s.smallestDistancePair([1, 1, 1], 2) == 0
    assert s.smallestDistancePair([1, 6, 1], 3) == 5
    assert s.smallestDistancePair([1, 2, 3, 4], 3) == 1
    assert s.smallestDistancePair([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18) == 2

    cases = [
        ([1, 3, 1], 1),
        ([1, 1, 1], 2),
        ([1, 6, 1], 3),
        ([1, 2, 3, 4], 3),
        ([1, 2, 3, 4], 6),
        ([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18),
        ([0, 0, 0, 0], 5),
        ([1, 1000000], 1),
        ([5, 5, 5, 5, 5, 5], 10),
        ([62, 100, 4], 2),
        ([38, 33, 57, 65, 13, 2, 86, 75], 20),
        ([1, 4, 9, 16, 25, 36], 7),
    ]

    # the heap merge shares no counting pass and no monotonicity claim with the
    # bisect, so agreement checks the two-pointer sweep rather than restating it
    for nums, k in cases:
        assert s.smallestDistancePairHeap(nums, k) == s.smallestDistancePair(nums, k), (
            nums,
            k,
        )

    # the witness is one of possibly many pairs at that distance, so it gets
    # checked on the property - the distance matches, and both values are
    # present in the input
    for nums, k in cases:
        ans, (a, b) = s.smallestDistancePairWitness(nums, k)
        assert b - a == ans, (nums, k, a, b)
        assert a in nums and b in nums, (nums, k, a, b)
        assert ans == s.smallestDistancePair(nums, k), (nums, k)

    # k == 1 means no search happens, so the general path has to land on the
    # plain adjacent minimum
    for nums in [[1, 3, 1], [1, 2, 3, 4], [62, 100, 4], [0, 0, 0, 0], [1, 1000000]]:
        assert s.smallestDistancePair(nums, 1) == s.smallestDistancePairMinGap(nums, 1), nums

    assert s.smallestDistancePairMinGap([1, 2, 3], 2) is None

    # the counting pass on its own, against the definition it is supposed to
    # compute. this is the part the bisect cannot check, since a c that is wrong
    # but still monotone would produce a confident wrong boundary
    def count_brute(nums, limit):
        nums = sorted(nums)
        return sum(
            1
            for i in range(len(nums))
            for j in range(i + 1, len(nums))
            if nums[j] - nums[i] <= limit
        )

    for nums, _ in cases:
        for limit in range(0, max(nums) - min(nums) + 2):
            assert s._count_within(sorted(nums), limit) == count_brute(nums, limit), (
                nums,
                limit,
            )

    # and the full multiset built and sorted, which is the only check that tests
    # the order-statistic claim itself rather than the search around it
    def brute(nums, k):
        distances = sorted(
            abs(nums[j] - nums[i])
            for i in range(len(nums))
            for j in range(i + 1, len(nums))
        )
        return distances[k - 1]

    for nums, k in cases:
        assert s.smallestDistancePair(nums, k) == brute(nums, k), (nums, k)

    # every k on a handful of arrays, so the boundary is walked across the whole
    # multiset instead of sampled at one point. this is where an off-by-one in
    # "smallest x with c(x) >= k" would show up
    for nums in [[1, 3, 1], [1, 2, 3, 4], [9, 10, 7, 6, 1], [4, 4, 9, 2], [1, 5, 9, 13]]:
        total = len(nums) * (len(nums) - 1) // 2
        for k in range(1, total + 1):
            assert s.smallestDistancePair(nums, k) == brute(nums, k), (nums, k)

    print("all good")
