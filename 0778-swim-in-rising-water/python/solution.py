from typing import List
import heapq

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        seen = {(0, 0)}
        h = [(grid[0][0], 0, 0)]
        ans = 0
        while h:
            t, r, c = heapq.heappop(h)
            ans = max(ans, t)
            if (r, c) == (n - 1, n - 1):
                return ans
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    heapq.heappush(h, (grid[nr][nc], nr, nc))
        return -1
