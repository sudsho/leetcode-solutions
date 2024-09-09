from typing import List

class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        ans = 0
        mask = 0
        for bit in range(29, -1, -1):
            mask |= 1 << bit
            cur = -1
            ops = 0
            for x in nums:
                cur &= x & mask
                if cur & ~ans:
                    ops += 1
                else:
                    cur = -1
            if ops > k:
                ans |= 1 << bit
        return ans
# corrected edge case
