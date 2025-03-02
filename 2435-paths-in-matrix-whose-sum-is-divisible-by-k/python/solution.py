from typing import List

class Solution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        MOD = 10 ** 9 + 7
        m, n = len(grid), len(grid[0])
        dp = [[[0] * k for _ in range(n)] for _ in range(m)]
        dp[0][0][grid[0][0] % k] = 1
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                cur = grid[i][j] % k
                for r in range(k):
                    prev = (r - cur) % k
                    s = 0
                    if i:
                        s += dp[i - 1][j][prev]
                    if j:
                        s += dp[i][j - 1][prev]
                    dp[i][j][r] = s % MOD
        return dp[m - 1][n - 1][0]
