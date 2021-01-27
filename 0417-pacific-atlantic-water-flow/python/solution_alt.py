# alt: DFS from each ocean, intersect reachable sets
from typing import List

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights:
            return []
        m, n = len(heights), len(heights[0])
        pac = set()
        atl = set()

        def dfs(r: int, c: int, seen: set) -> None:
            seen.add((r, c))
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    dfs(nr, nc, seen)

        for i in range(m):
            dfs(i, 0, pac)
            dfs(i, n - 1, atl)
        for j in range(n):
            dfs(0, j, pac)
            dfs(m - 1, j, atl)

        return [[r, c] for r, c in pac & atl]
