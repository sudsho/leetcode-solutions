"""
72. Edit Distance (Hard)
Given two strings word1 and word2, return the minimum number of operations
(insert, delete, or replace a character) required to convert word1 to word2.
"""


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)

        # dp[i][j] = edit distance between word1[:i] and word2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # delete from word1
                        dp[i][j - 1],      # insert into word1
                        dp[i - 1][j - 1],  # replace
                    )

        return dp[m][n]

    def minDistanceOptimized(self, word1: str, word2: str) -> int:
        # space-optimized: only keep previous row
        m, n = len(word1), len(word2)
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m

        prev = list(range(n + 1))
        for i in range(1, m + 1):
            curr = [i] + [0] * n
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
            prev = curr
        return prev[n]


# Time: O(m * n)
# Space: O(m * n) for the 2D table, O(min(m, n)) for the optimized version


if __name__ == "__main__":
    sol = Solution()
    print(sol.minDistance("horse", "ros"))      # 3
    print(sol.minDistance("intention", "execution"))  # 5
    print(sol.minDistanceOptimized("abc", "abc"))     # 0
