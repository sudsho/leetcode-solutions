from typing import List

class Solution:
    def validSubarrays(self, nums: List[int]) -> int:
        # Right-to-left next-smaller using monotonic stack
        n = len(nums)
        next_smaller = [n] * n
        stack: list[int] = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            if stack:
                next_smaller[i] = stack[-1]
            stack.append(i)
        return sum(next_smaller[i] - i for i in range(n))
