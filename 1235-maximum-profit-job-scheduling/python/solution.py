from typing import List
from bisect import bisect_right

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        jobs = sorted(zip(endTime, startTime, profit))
        ends = [j[0] for j in jobs]
        n = len(jobs)
        dp = [0] * (n + 1)
        for i, (e, s, p) in enumerate(jobs, 1):
            j = bisect_right(ends, s, 0, i - 1)
            dp[i] = max(dp[i - 1], dp[j] + p)
        return dp[n]
