# alt: 1D rolling
from typing import List

class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])
        dp = [float('inf')] * (n + 1)
        dp[n - 1] = 1
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                right = dp[j + 1] if j + 1 <= n else float('inf')
                down = dp[j] if i < m - 1 else (1 if j == n - 1 else float('inf'))
                need = min(right, down) - dungeon[i][j]
                dp[j] = max(1, need)
        return int(dp[0])
