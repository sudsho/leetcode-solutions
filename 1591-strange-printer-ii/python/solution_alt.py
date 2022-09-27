# layered DFS with cycle detection
from typing import List
from collections import defaultdict

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
        for color, (r1, c1, r2, c2) in bbox.items():
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    other = targetGrid[r][c]
                    if other != color:
                        graph[color].add(other)
        # detect cycle via dfs
        WHITE, GRAY, BLACK = 0, 1, 2
        state = {c: WHITE for c in bbox}

        def dfs(c: int) -> bool:
            state[c] = GRAY
            for nb in graph[c]:
                if state[nb] == GRAY:
                    return False
                if state[nb] == WHITE and not dfs(nb):
                    return False
            state[c] = BLACK
            return True

        for c in bbox:
            if state[c] == WHITE and not dfs(c):
                return False
        return True
