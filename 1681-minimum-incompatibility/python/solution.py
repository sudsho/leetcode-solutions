from typing import List
from collections import Counter

class Solution:
    def minimumIncompatibility(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if any(v > k for v in Counter(nums).values()):
            return -1
        size = n // k
        # for every subset of size==size with all unique, compute cost
        INF = 1 << 30
        cost: dict[int, int] = {}
        for mask in range(1 << n):
            if bin(mask).count('1') != size:
                continue
            seen: set[int] = set()
            mn, mx = 1 << 30, -1
            ok = True
            for j in range(n):
                if mask >> j & 1:
                    if nums[j] in seen:
                        ok = False
                        break
                    seen.add(nums[j])
                    mn = min(mn, nums[j])
                    mx = max(mx, nums[j])
            if ok:
                cost[mask] = mx - mn
        dp = [INF] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            if dp[mask] == INF:
                continue
            # find first zero bit
            sub = ((1 << n) - 1) ^ mask
            j = sub & -sub  # lowest bit set in remaining
            # enumerate subsets of `sub` containing j
            s = sub
            ss = s
            while ss:
                if ss & j and ss in cost:
                    if dp[mask] + cost[ss] < dp[mask | ss]:
                        dp[mask | ss] = dp[mask] + cost[ss]
                ss = (ss - 1) & s
        return -1 if dp[(1 << n) - 1] == INF else dp[(1 << n) - 1]
