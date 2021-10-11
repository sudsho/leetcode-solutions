from typing import List

class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        a = [1] + nums + [1]
        n = len(a)
        dp = [[0] * n for _ in range(n)]
        for length in range(2, n):
            for l in range(n - length):
                r = l + length
                for k in range(l + 1, r):
                    dp[l][r] = max(dp[l][r], a[l] * a[k] * a[r] + dp[l][k] + dp[k][r])
        return dp[0][n - 1]
# typing fix
