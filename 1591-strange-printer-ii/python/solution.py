from typing import List
from collections import defaultdict, deque

class Solution:
    def isPrintable(self, targetGrid: List[List[int]]) -> bool:
        rows, cols = len(targetGrid), len(targetGrid[0])
        bbox: dict = {}
        for r in range(rows):
            for c in range(cols):
                color = targetGrid[r][c]
                if color not in bbox:
                    bbox[color] = [r, c, r, c]
                else:
                    b = bbox[color]
                    b[0] = min(b[0], r)
                    b[1] = min(b[1], c)
                    b[2] = max(b[2], r)
                    b[3] = max(b[3], c)
        graph = defaultdict(set)
        indeg = {c: 0 for c in bbox}
        for color, (r1, c1, r2, c2) in bbox.items():
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    other = targetGrid[r][c]
                    if other != color and color not in graph[other]:
                        graph[other].add(color)
                        indeg[color] += 1
        q = deque(c for c, d in indeg.items() if d == 0)
        seen = 0
        while q:
            x = q.popleft()
            seen += 1
            for y in graph[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    q.append(y)
        return seen == len(bbox)
