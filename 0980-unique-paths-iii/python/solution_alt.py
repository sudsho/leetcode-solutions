# alt: revisited in 2023, slight cleanup
from typing import List, Optional

# original idea kept; this version uses match/dataclass-style refactor where it helps.

from typing import List

class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        empty = 1
        sr = sc = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    empty += 1
                elif grid[r][c] == 1:
                    sr, sc = r, c

        ans = 0

        def dfs(r: int, c: int, remaining: int) -> None:
            nonlocal ans
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == -1:
                return
            if grid[r][c] == 2:
                if remaining == 0:
                    ans += 1
                return
            grid[r][c] = -1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                dfs(r + dr, c + dc, remaining - 1)
            grid[r][c] = 0

        dfs(sr, sc, empty)
        return ans
