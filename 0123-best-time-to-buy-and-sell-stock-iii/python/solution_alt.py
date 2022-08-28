# dp[k][i] table version, easier to read
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        K = 2
        n = len(prices)
        if n < 2:
            return 0
        dp = [[0] * n for _ in range(K + 1)]
        for k in range(1, K + 1):
            min_cost = prices[0]
            for i in range(1, n):
                min_cost = min(min_cost, prices[i] - dp[k - 1][i - 1])
                dp[k][i] = max(dp[k][i - 1], prices[i] - min_cost)
        return dp[K][n - 1]
