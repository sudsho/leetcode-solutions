from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        # sliding window: grow right, shrink left while window sum >= target
        left = 0
        window_sum = 0
        best = len(nums) + 1
        for right in range(len(nums)):
            window_sum += nums[right]
            while window_sum >= target:
                best = min(best, right - left + 1)
                window_sum -= nums[left]
                left += 1
        return best if best <= len(nums) else 0
