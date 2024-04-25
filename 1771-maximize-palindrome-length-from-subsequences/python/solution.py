class Solution:
    def longestPalindrome(self, word1: str, word2: str) -> int:
        s = word1 + word2
        n = len(s)
        n1 = len(word1)
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = 1
        best = 0
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
                    if i < n1 <= j:
                        best = max(best, dp[i][j])
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return best
# minor cleanup
