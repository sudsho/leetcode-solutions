from typing import List
from functools import lru_cache

class Solution:
    def minTaps(self, n: int, ranges: List[int]) -> int:
        # DP variant: dp[i] = min taps to cover [0, i]
        intervals = sorted((max(0, i - r), min(n, i + r)) for i, r in enumerate(ranges))
        INF = 10 ** 9
        dp = [INF] * (n + 1)
        dp[0] = 0
        for left, right in intervals:
            if dp[left] == INF:
                continue
            for j in range(left + 1, right + 1):
                if dp[left] + 1 < dp[j]:
                    dp[j] = dp[left] + 1
        return dp[n] if dp[n] < INF else -1
