from typing import List
from math import gcd

class Solution:
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        present = set(nums)
        max_v = max(nums)
        result = 0
        for g in range(1, max_v + 1):
            current = 0
            for m in range(g, max_v + 1, g):
                if m in present:
                    current = gcd(current, m)
                    if current == g:
                        result += 1
                        break
        return result
