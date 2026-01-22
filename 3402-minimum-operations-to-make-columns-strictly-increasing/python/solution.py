from typing import List


class Solution:
    def minimumOperations(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0]) if rows else 0
        ops = 0
        for c in range(cols):
            prev = grid[0][c]
            for r in range(1, rows):
                need = prev + 1
                if grid[r][c] < need:
                    ops += need - grid[r][c]
                    prev = need
                else:
                    prev = grid[r][c]
        return ops
