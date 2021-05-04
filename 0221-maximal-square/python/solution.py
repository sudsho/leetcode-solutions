from typing import List

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0])
        dp = [0] * (n + 1)
        best = 0
        for i in range(m):
            new = [0] * (n + 1)
            for j in range(n):
                if matrix[i][j] == "1":
                    new[j + 1] = 1 + min(dp[j], dp[j + 1], new[j])
                    best = max(best, new[j + 1])
            dp = new
        return best * best
