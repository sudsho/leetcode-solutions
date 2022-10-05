from typing import List
from bisect import bisect_right

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort(key=lambda e: e[1])
        ends = [e[1] for e in events]
        n = len(events)
        dp = [[0] * (k + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            s, e, v = events[i - 1]
            j = bisect_right(ends, s - 1, 0, i - 1)
            for c in range(1, k + 1):
                dp[i][c] = max(dp[i - 1][c], dp[j][c - 1] + v)
        return dp[n][k]
