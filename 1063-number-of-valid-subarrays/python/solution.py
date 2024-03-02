from typing import List

class Solution:
    def validSubarrays(self, nums: List[int]) -> int:
        stack: list[int] = []
        ans = 0
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] > x:
                ans += i - stack.pop()
            stack.append(i)
        n = len(nums)
        while stack:
            ans += n - stack.pop()
        return ans
# tightened naming
# corrected edge case
