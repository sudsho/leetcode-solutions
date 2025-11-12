from typing import List
from collections import Counter

class Solution:
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        n = len(nums)
        total = n * (n + 1) // 2
        target = (total + 1) // 2

        def count_at_most(k: int) -> int:
            cnt: Counter = Counter()
            l = 0
            res = 0
            for r in range(n):
                cnt[nums[r]] += 1
                while len(cnt) > k:
                    cnt[nums[l]] -= 1
                    if cnt[nums[l]] == 0:
                        del cnt[nums[l]]
                    l += 1
                res += r - l + 1
            return res

        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if count_at_most(mid) >= target:
                hi = mid
            else:
                lo = mid + 1
        return lo
