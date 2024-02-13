from typing import List

class Solution:
    def containVirus(self, isInfected: List[List[int]]) -> int:
        m, n = len(isInfected), len(isInfected[0])
        walls = 0
        while True:
            visited = [[False] * n for _ in range(m)]
            regions: list[set[tuple[int, int]]] = []
            frontiers: list[set[tuple[int, int]]] = []
            wall_counts: list[int] = []
            for i in range(m):
                for j in range(n):
                    if isInfected[i][j] == 1 and not visited[i][j]:
                        region: set[tuple[int, int]] = set()
                        frontier: set[tuple[int, int]] = set()
                        wc = 0
                        stack = [(i, j)]
                        visited[i][j] = True
                        while stack:
                            x, y = stack.pop()
                            region.add((x, y))
                            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < m and 0 <= ny < n:
                                    if isInfected[nx][ny] == 1 and not visited[nx][ny]:
                                        visited[nx][ny] = True
                                        stack.append((nx, ny))
                                    elif isInfected[nx][ny] == 0:
                                        frontier.add((nx, ny))
                                        wc += 1
                        regions.append(region)
                        frontiers.append(frontier)
                        wall_counts.append(wc)
            if not regions:
                return walls
            best = max(range(len(frontiers)), key=lambda i: len(frontiers[i]))
            walls += wall_counts[best]
            for k, region in enumerate(regions):
                if k == best:
                    for x, y in region:
                        isInfected[x][y] = 2
                else:
                    for x, y in frontiers[k]:
                        isInfected[x][y] = 1
        return walls
