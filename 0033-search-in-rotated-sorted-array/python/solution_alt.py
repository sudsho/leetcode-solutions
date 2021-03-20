# alt: find pivot first, then binary search the right half
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] > nums[hi]:
                lo = mid + 1
            else:
                hi = mid
        pivot = lo
        # binary search in two halves
        for l, r in ((0, pivot - 1), (pivot, len(nums) - 1)):
            while l <= r:
                m = (l + r) // 2
                if nums[m] == target:
                    return m
                if nums[m] < target:
                    l = m + 1
                else:
                    r = m - 1
        return -1
