# alt: dp[i][j] min of max sum splitting first i into j pieces
from typing import List

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        pre = [0] * (n + 1)
        for i, x in enumerate(nums):
            pre[i + 1] = pre[i] + x
        INF = float('inf')
        dp = [[INF] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for p in range(i):
                    dp[i][j] = min(dp[i][j], max(dp[p][j - 1], pre[i] - pre[p]))
        return int(dp[n][k])
