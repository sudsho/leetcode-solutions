from typing import List
from collections import deque
import heapq

class Solution:
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
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
        # max-min path Dijkstra
        heap: list[tuple[int, int, int]] = [(-dist[0][0], 0, 0)]
        seen = [[False] * n for _ in range(n)]
        while heap:
            neg_safe, x, y = heapq.heappop(heap)
            if seen[x][y]:
                continue
            seen[x][y] = True
            if (x, y) == (n - 1, n - 1):
                return -neg_safe
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and not seen[nx][ny]:
                    heapq.heappush(heap, (-min(-neg_safe, dist[nx][ny]), nx, ny))
        return 0
# tightened naming
# minor cleanup
