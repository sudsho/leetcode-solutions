# alt: bottom-up dp[len][i][j]
class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        n = len(s1)
        if n != len(s2):
            return False
        dp = [[[False] * n for _ in range(n)] for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                dp[1][i][j] = s1[i] == s2[j]
        for L in range(2, n + 1):
            for i in range(n - L + 1):
                for j in range(n - L + 1):
                    for k in range(1, L):
                        if dp[k][i][j] and dp[L - k][i + k][j + k]:
                            dp[L][i][j] = True
                            break
                        if dp[k][i][j + L - k] and dp[L - k][i + k][j]:
                            dp[L][i][j] = True
                            break
        return dp[n][0][0]
