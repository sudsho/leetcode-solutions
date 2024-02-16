from typing import List
from collections import deque

class Solution:
    def containVirus(self, isInfected: List[List[int]]) -> int:
        # BFS-flavored exploration: same idea, queue-based traversal
        m, n = len(isInfected), len(isInfected[0])
        walls = 0
        DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
        while True:
            visited = [[False] * n for _ in range(m)]
            regions: list[list[tuple[int, int]]] = []
            frontiers: list[set[tuple[int, int]]] = []
            wall_counts: list[int] = []
            for i in range(m):
                for j in range(n):
                    if isInfected[i][j] != 1 or visited[i][j]:
                        continue
                    region: list[tuple[int, int]] = []
                    frontier: set[tuple[int, int]] = set()
                    wc = 0
                    q: deque[tuple[int, int]] = deque([(i, j)])
                    visited[i][j] = True
                    while q:
                        x, y = q.popleft()
                        region.append((x, y))
                        for dx, dy in DIRS:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < m and 0 <= ny < n:
                                if isInfected[nx][ny] == 1 and not visited[nx][ny]:
                                    visited[nx][ny] = True
                                    q.append((nx, ny))
                                elif isInfected[nx][ny] == 0:
                                    frontier.add((nx, ny))
                                    wc += 1
                    regions.append(region)
                    frontiers.append(frontier)
                    wall_counts.append(wc)
            if not regions:
                return walls
            best = max(range(len(frontiers)), key=lambda k: len(frontiers[k]))
            walls += wall_counts[best]
            for k, region in enumerate(regions):
                if k == best:
                    for x, y in region:
                        isInfected[x][y] = 2
                else:
                    for x, y in frontiers[k]:
                        isInfected[x][y] = 1
