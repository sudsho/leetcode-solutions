from typing import List

class Solution:
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        max_seen = float("-inf")
        min_seen = float("inf")
        l, r = 0, -1
        for i in range(n):
            max_seen = max(max_seen, nums[i])
            if nums[i] < max_seen:
                r = i
            min_seen = min(min_seen, nums[n - 1 - i])
            if nums[n - 1 - i] > min_seen:
                l = n - 1 - i
        return r - l + 1
