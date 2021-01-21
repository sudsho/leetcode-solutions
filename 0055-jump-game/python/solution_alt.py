# greedy with running max (clean variant)
from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        reach = 0
        for i, x in enumerate(nums):
            if i > reach:
                return False
            if i + x > reach:
                reach = i + x
        return True
