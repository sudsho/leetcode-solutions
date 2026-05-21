class Solution:
    def minPathSum(self, grid):
        # classic dp, can only move right or down so each cell
        # only depends on the one above and the one to the left
        m, n = len(grid), len(grid[0])
        # roll a 1d row of size n, updating left-to-right
        dp = [0] * n
        dp[0] = grid[0][0]
        for j in range(1, n):
            dp[j] = dp[j - 1] + grid[0][j]
        for i in range(1, m):
            dp[0] += grid[i][0]
            for j in range(1, n):
                dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]
        return dp[-1]
