# dfs each addLand to recount; not ideal but simple
from typing import List, Set

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        grid = [[0] * n for _ in range(m)]
        result: List[int] = []
        for r, c in positions:
            grid[r][c] = 1
            visited: Set[tuple] = set()
            count = 0
            for i in range(m):
                for j in range(n):
                    if grid[i][j] and (i, j) not in visited:
                        count += 1
                        stack = [(i, j)]
                        while stack:
                            x, y = stack.pop()
                            if (x, y) in visited:
                                continue
                            visited.add((x, y))
                            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] and (nx, ny) not in visited:
                                    stack.append((nx, ny))
            result.append(count)
        return result
