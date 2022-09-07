from typing import List

class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        n = len(prices)
        if n == 0 or k == 0:
            return 0
        if k >= n // 2:
            return sum(max(0, prices[i + 1] - prices[i]) for i in range(n - 1))
        buy = [float("inf")] * (k + 1)
        sell = [0] * (k + 1)
        for p in prices:
            for j in range(1, k + 1):
                buy[j] = min(buy[j], p - sell[j - 1])
                sell[j] = max(sell[j], p - buy[j])
        return int(sell[k])
