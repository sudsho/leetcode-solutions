# divide and conquer fallback - find min in each half
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        def helper(lo: int, hi: int) -> int:
            if lo == hi:
                return nums[lo]
            if hi - lo == 1:
                return min(nums[lo], nums[hi])
            if nums[lo] < nums[hi]:
                return nums[lo]
            mid = (lo + hi) // 2
            return min(helper(lo, mid), helper(mid + 1, hi))
        return helper(0, len(nums) - 1)
