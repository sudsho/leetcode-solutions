class Solution:
    def maxProfit(self, prices):
        # any time price goes up, harvest the delta - equivalent to
        # buying at every local min and selling at every local max
        # but you don't actually need to track those points.
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                profit += prices[i] - prices[i-1]
        return profit
