class Solution:
    def searchInsert(self, nums, target):
        """Binary search for target in a sorted array; if it is absent, return
        the index where it would be inserted to keep the array sorted. When the
        loop exits, lo has landed on exactly that insertion point."""
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        # lo is now the insertion point
        return lo
