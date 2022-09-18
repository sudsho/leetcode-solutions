# state machine flavor - same complexity, easier to read
from typing import List

class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        if not prices or k == 0:
            return 0
        n = len(prices)
        if k * 2 >= n:
            return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
        # dp[t][0] holding cash, dp[t][1] holding share
        dp = [[0, -prices[0]] for _ in range(k + 1)]
        for i in range(1, n):
            for t in range(k, 0, -1):
                dp[t][1] = max(dp[t][1], dp[t - 1][0] - prices[i])
                dp[t][0] = max(dp[t][0], dp[t][1] + prices[i])
        return dp[k][0]
