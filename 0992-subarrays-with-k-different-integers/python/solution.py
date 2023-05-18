from collections import Counter
from typing import List

class Solution:
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        def at_most(K: int) -> int:
            c: Counter = Counter()
            l = 0
            ans = 0
            for r, x in enumerate(nums):
                c[x] += 1
                while len(c) > K:
                    c[nums[l]] -= 1
                    if c[nums[l]] == 0:
                        del c[nums[l]]
                    l += 1
                ans += r - l + 1
            return ans
        return at_most(k) - at_most(k - 1)
