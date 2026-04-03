# Given prices array where prices[i] is stock price on day i,
# return maximum profit from one buy and one sell.
# Track the minimum price seen so far, update max profit at each step.

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price

        return max_profit

# Time: O(n) - single pass through prices
# Space: O(1) - only two variables tracked

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxProfit([7, 1, 5, 3, 6, 4]))   # 5 (buy at 1, sell at 6)
    print(sol.maxProfit([7, 6, 4, 3, 1]))        # 0 (prices always falling)
    print(sol.maxProfit([1, 2]))                  # 1
