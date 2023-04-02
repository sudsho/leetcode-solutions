# 2023 nit (55)
# iterative bottom-up table - skips lru_cache overhead
from typing import List

class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        NEG = -1
        # dp[r][c1][c2]
        dp = [[[NEG] * cols for _ in range(cols)] for _ in range(rows)]
        dp[0][0][cols - 1] = grid[0][0] + (grid[0][cols - 1] if cols - 1 != 0 else 0)
        for r in range(1, rows):
            for c1 in range(cols):
                for c2 in range(cols):
                    best = NEG
                    for d1 in (-1, 0, 1):
                        for d2 in (-1, 0, 1):
                            pc1 = c1 - d1
                            pc2 = c2 - d2
                            if 0 <= pc1 < cols and 0 <= pc2 < cols and dp[r - 1][pc1][pc2] != NEG:
                                if dp[r - 1][pc1][pc2] > best:
                                    best = dp[r - 1][pc1][pc2]
                    if best == NEG:
                        continue
                    cur = grid[r][c1] + (grid[r][c2] if c1 != c2 else 0)
                    dp[r][c1][c2] = best + cur
        result = 0
        for c1 in range(cols):
            for c2 in range(cols):
                if dp[rows - 1][c1][c2] > result:
                    result = dp[rows - 1][c1][c2]
        return result
