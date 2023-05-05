# alt: revisited in 2023, slight cleanup
from typing import List, Optional

# original idea kept; this version uses match/dataclass-style refactor where it helps.

from typing import List
from functools import lru_cache

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        m, n = len(matrix), len(matrix[0])

        @lru_cache(None)
        def dfs(r: int, c: int) -> int:
            best = 1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            return best

        return max(dfs(r, c) for r in range(m) for c in range(n))
