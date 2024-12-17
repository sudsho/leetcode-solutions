from functools import lru_cache

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # dp[i][j] = start index of shortest window in s[:i+1] matching t[:j+1]
        n, m = len(s), len(t)
        dp = [[-1] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if s[i - 1] == t[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = dp[i - 1][j]
        start, length = 0, n + 1
        for i in range(1, n + 1):
            if dp[i][m] != -1 and i - dp[i][m] < length:
                start = dp[i][m]
                length = i - dp[i][m]
        return "" if length == n + 1 else s[start:start + length]
