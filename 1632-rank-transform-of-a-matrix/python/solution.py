from typing import List
from collections import defaultdict

class DSU:
    def __init__(self) -> None:
        self.p: dict = {}

    def find(self, x):
        if self.p.setdefault(x, x) != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)

class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        groups = defaultdict(list)
        for r in range(rows):
            for c in range(cols):
                groups[matrix[r][c]].append((r, c))
        row_rank = [0] * rows
        col_rank = [0] * cols
        result = [[0] * cols for _ in range(rows)]
        for v in sorted(groups):
            dsu = DSU()
            for r, c in groups[v]:
                dsu.union(("r", r), ("c", c))
            buckets = defaultdict(list)
            for r, c in groups[v]:
                buckets[dsu.find(("r", r))].append((r, c))
            for cells in buckets.values():
                rank = 1
                for r, c in cells:
                    rank = max(rank, row_rank[r] + 1, col_rank[c] + 1)
                for r, c in cells:
                    result[r][c] = rank
                    row_rank[r] = max(row_rank[r], rank)
                    col_rank[c] = max(col_rank[c], rank)
        return result
