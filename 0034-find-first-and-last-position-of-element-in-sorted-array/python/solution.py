"""LeetCode 34 - Find First and Last Position of Element in Sorted Array."""
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        lo = self._lower_bound(nums, target)
        if lo == len(nums) or nums[lo] != target:
            return [-1, -1]
        hi = self._lower_bound(nums, target + 1) - 1
        return [lo, hi]

    @staticmethod
    def _lower_bound(nums: List[int], target: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]),
        ([1], 1, [0, 0]),
        ([2, 2, 2, 2, 2], 2, [0, 4]),
        ([1, 2, 3], 4, [-1, -1]),
    ]
    for nums, t, want in cases:
        got = s.searchRange(nums, t)
        assert got == want, f"{nums} {t} -> {got}, want {want}"
    print("ok")
