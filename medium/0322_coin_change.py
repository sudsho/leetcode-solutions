# Given an array of coin denominations and a target amount,
# return the fewest number of coins needed to make up that amount.
# Return -1 if the amount cannot be made with the given coins.

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        # Bottom-up DP: dp[i] = min coins to make amount i
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

# Time:  O(amount * len(coins))
# Space: O(amount)

if __name__ == "__main__":
    sol = Solution()

    # Example 1: coins = [1, 5, 10, 25], amount = 41 → 3 (25 + 10 + 5 + 1 = nope, 25+10+5+1=41 → 4)
    print(sol.coinChange([1, 5, 10, 25], 41))  # 4

    # Example 2: classic [1, 2, 5], amount = 11 → 3 (5 + 5 + 1)
    print(sol.coinChange([1, 2, 5], 11))  # 3

    # Example 3: impossible case
    print(sol.coinChange([2], 3))  # -1
