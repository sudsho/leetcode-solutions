from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_line(arr: List[int]) -> int:
            prev = curr = 0
            for x in arr:
                prev, curr = curr, max(curr, prev + x)
            return curr

        return max(rob_line(nums[1:]), rob_line(nums[:-1]))
