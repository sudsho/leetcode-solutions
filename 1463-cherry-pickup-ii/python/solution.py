from typing import List
from functools import lru_cache

class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])

        @lru_cache(maxsize=None)
        def dp(r: int, c1: int, c2: int) -> int:
            if c1 < 0 or c1 >= cols or c2 < 0 or c2 >= cols:
                return -1
            cherries = grid[r][c1] + (grid[r][c2] if c1 != c2 else 0)
            if r == rows - 1:
                return cherries
            best = 0
            for d1 in (-1, 0, 1):
                for d2 in (-1, 0, 1):
                    sub = dp(r + 1, c1 + d1, c2 + d2)
                    if sub > best:
                        best = sub
            return cherries + best
        return dp(0, 0, cols - 1)
