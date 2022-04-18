# brute force per-hit - too slow for large N, kept for reference
from typing import List

class Solution:
    def hitBricks(self, grid: List[List[int]], hits: List[List[int]]) -> List[int]:
        rows, cols = len(grid), len(grid[0])
        g = [row[:] for row in grid]

        def reachable_count() -> int:
            seen = [[False] * cols for _ in range(rows)]
            stack = []
            for c in range(cols):
                if g[0][c]:
                    stack.append((0, c))
                    seen[0][c] = True
            count = 0
            while stack:
                r, c = stack.pop()
                count += 1
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            return count

        result: List[int] = []
        for r, c in hits:
            if g[r][c] == 0:
                result.append(0)
                continue
            before = reachable_count()
            g[r][c] = 0
            after = reachable_count()
            result.append(max(0, before - after - 1))
        return result
