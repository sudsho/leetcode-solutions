from typing import List
from collections import deque

class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        if m + n - 2 <= k:
            return m + n - 2
        seen = {(0, 0, k)}
        q = deque([(0, 0, k, 0)])
        while q:
            r, c, kk, d = q.popleft()
            if (r, c) == (m - 1, n - 1):
                return d
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nk = kk - grid[nr][nc]
                    if nk >= 0 and (nr, nc, nk) not in seen:
                        seen.add((nr, nc, nk))
                        q.append((nr, nc, nk, d + 1))
        return -1
