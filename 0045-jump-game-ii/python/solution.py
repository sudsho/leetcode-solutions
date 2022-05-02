from typing import List

class Solution:
    def jump(self, nums: List[int]) -> int:
        jumps = reach = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == reach:
                jumps += 1
                reach = farthest
        return jumps
