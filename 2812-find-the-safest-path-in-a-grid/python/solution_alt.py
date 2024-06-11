from typing import List
from collections import deque

class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        # Binary-search the safeness threshold + BFS
        n = len(grid)
        if grid[0][0] or grid[n - 1][n - 1]:
            return 0
        dist = [[-1] * n for _ in range(n)]
        q: deque[tuple[int, int]] = deque()
        for i in range(n):
            for j in range(n):
                if grid[i][j]:
                    dist[i][j] = 0
                    q.append((i, j))
        while q:
            x, y = q.popleft()
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

        def reachable(thr: int) -> bool:
            if dist[0][0] < thr:
                return False
            seen = [[False] * n for _ in range(n)]
            seen[0][0] = True
            stack = [(0, 0)]
            while stack:
                x, y = stack.pop()
                if (x, y) == (n - 1, n - 1):
                    return True
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not seen[nx][ny] and dist[nx][ny] >= thr:
                        seen[nx][ny] = True
                        stack.append((nx, ny))
            return False
        lo, hi = 0, 2 * n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if reachable(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
