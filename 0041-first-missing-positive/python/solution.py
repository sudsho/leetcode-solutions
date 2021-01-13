from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        while i < n:
            v = nums[i]
            if 1 <= v <= n and nums[v - 1] != v:
                nums[v - 1], nums[i] = nums[i], nums[v - 1]
            else:
                i += 1
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1
