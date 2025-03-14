from typing import List

class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        ans = 0
        last_min = last_max = -1
        invalid = -1
        for i, x in enumerate(nums):
            if x < minK or x > maxK:
                invalid = i
            if x == minK:
                last_min = i
            if x == maxK:
                last_max = i
            ans += max(0, min(last_min, last_max) - invalid)
        return ans
