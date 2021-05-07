# alt with bitmask trick (very fast in Python for small targets)
from typing import List

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False
        target = total // 2
        bits = 1
        for n in nums:
            bits |= bits << n
        return (bits >> target) & 1 == 1
