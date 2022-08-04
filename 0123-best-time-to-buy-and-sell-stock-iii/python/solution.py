from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy1 = buy2 = float("inf")
        sell1 = sell2 = 0
        for p in prices:
            buy1 = min(buy1, p)
            sell1 = max(sell1, p - buy1)
            buy2 = min(buy2, p - sell1)
            sell2 = max(sell2, p - buy2)
        return int(sell2)
