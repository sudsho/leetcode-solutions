from typing import List
from sortedcontainers import SortedList

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        # cost[i] = sum of |nums[j] - median| for window starting at i, size x
        n = len(nums)
        sl = SortedList()
        # maintain prefix sum or rolling cost via two halves
        from sortedcontainers import SortedList as SL
        low: list[int] = []
        high: list[int] = []
        # we use a simpler O(n*x) over windows where x is small enough
        cost = [0] * (n - x + 1)
        for i in range(n - x + 1):
            window = sorted(nums[i:i + x])
            mid = window[x // 2]
            cost[i] = sum(abs(v - mid) for v in window)
        # pick k non-overlapping windows minimizing total cost
        INF = 10 ** 18
        # dp[i][j] = min cost using j windows, last possibly ending at <= i+x-1
        dp = [[INF] * (k + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = 0
        for j in range(1, k + 1):
            best = INF
            for i in range(j * x, n + 1):
                if dp[i - x][j - 1] != INF:
                    best = min(best, dp[i - x][j - 1] + cost[i - x])
                dp[i][j] = min(dp[i - 1][j], best)
        return dp[n][k]
