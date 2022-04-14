from typing import List

class DSU:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.size[ra] += self.size[rb]

    def comp_size(self, x: int) -> int:
        return self.size[self.find(x)]

class Solution:
    def hitBricks(self, grid: List[List[int]], hits: List[List[int]]) -> List[int]:
        rows, cols = len(grid), len(grid[0])
        g = [row[:] for row in grid]
        for r, c in hits:
            g[r][c] = 0
        TOP = rows * cols
        dsu = DSU(rows * cols + 1)

        def idx(r: int, c: int) -> int:
            return r * cols + c

        for c in range(cols):
            if g[0][c]:
                dsu.union(c, TOP)
        for r in range(1, rows):
            for c in range(cols):
                if g[r][c]:
                    if g[r - 1][c]:
                        dsu.union(idx(r, c), idx(r - 1, c))
                    if c and g[r][c - 1]:
                        dsu.union(idx(r, c), idx(r, c - 1))

        result = [0] * len(hits)
        for i in range(len(hits) - 1, -1, -1):
            r, c = hits[i]
            if grid[r][c] == 0:
                continue
            before = dsu.comp_size(TOP)
            g[r][c] = 1
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc]:
                    dsu.union(idx(r, c), idx(nr, nc))
            if r == 0:
                dsu.union(idx(r, c), TOP)
            after = dsu.comp_size(TOP)
            result[i] = max(0, after - before - 1)
        return result
