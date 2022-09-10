# sieve-flavor enumeration with dictionary count
from typing import List
from math import gcd

class Solution:
    def countDifferentSubsequenceGCDs(self, nums: List[int]) -> int:
        max_v = max(nums)
        present = [False] * (max_v + 1)
        for n in nums:
            present[n] = True
        out = 0
        for g in range(1, max_v + 1):
            cur = 0
            m = g
            while m <= max_v:
                if present[m]:
                    cur = gcd(cur, m)
                    if cur == g:
                        out += 1
                        break
                m += g
        return out
