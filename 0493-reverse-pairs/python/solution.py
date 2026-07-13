from typing import List

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        """Count pairs (i, j) with i < j and nums[i] > 2 * nums[j].

        Same skeleton as counting smaller-after-self (315): merge sort, and
        do the counting on each merge step while both halves are already
        sorted. The one twist is that the "> 2 * right" test does not line up
        with the merge comparison, so the count is a separate two-pointer
        sweep over the two sorted halves before they get merged.
        """

        def sort_and_count(lo: int, hi: int) -> int:
            if hi - lo <= 1:
                return 0
            mid = (lo + hi) // 2
            count = sort_and_count(lo, mid) + sort_and_count(mid, hi)

            # Both nums[lo:mid] and nums[mid:hi] are sorted ascending now.
            # For each left value, advance j while it still dominates 2*right.
            # j only moves forward across the whole left scan -> O(n) per level.
            j = mid
            for i in range(lo, mid):
                while j < hi and nums[i] > 2 * nums[j]:
                    j += 1
                count += j - mid

            nums[lo:hi] = sorted(nums[lo:hi])
            return count

        return sort_and_count(0, len(nums))
