from typing import List

class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        def count_islands(g):
            seen = set()
            m, n = len(g), len(g[0])
            cnt = 0
            for i in range(m):
                for j in range(n):
                    if g[i][j] == 1 and (i, j) not in seen:
                        cnt += 1
                        stack = [(i, j)]
                        while stack:
                            x, y = stack.pop()
                            if (x, y) in seen:
                                continue
                            seen.add((x, y))
                            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < m and 0 <= ny < n and g[nx][ny] == 1 and (nx, ny) not in seen:
                                    stack.append((nx, ny))
            return cnt
        if count_islands(grid) != 1:
            return 0
        m, n = len(grid), len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    grid[i][j] = 0
                    if count_islands(grid) != 1:
                        grid[i][j] = 1
                        return 1
                    grid[i][j] = 1
        return 2
