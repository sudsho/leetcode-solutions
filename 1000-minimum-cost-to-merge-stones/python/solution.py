# tweak 146
from typing import List

class Solution:
    def mergeStones(self, stones: List[int], k: int) -> int:
        n = len(stones)
        if (n - 1) % (k - 1) != 0:
            return -1
        pre = [0] * (n + 1)
        for i, x in enumerate(stones):
            pre[i + 1] = pre[i] + x
        INF = float('inf')
        dp = [[0] * n for _ in range(n)]
        for length in range(k, n + 1):
            for l in range(n - length + 1):
                r = l + length - 1
                dp[l][r] = INF
                m = l
                while m < r:
                    dp[l][r] = min(dp[l][r], dp[l][m] + dp[m + 1][r])
                    m += k - 1
                if (r - l) % (k - 1) == 0:
                    dp[l][r] += pre[r + 1] - pre[l]
        return int(dp[0][n - 1])
