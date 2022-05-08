# alternative: process by sorted value iteratively, no DSU
from typing import List
from collections import defaultdict

class Solution:
    def matrixRankTransform(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        cells = []
        for r in range(rows):
            for c in range(cols):
                cells.append((matrix[r][c], r, c))
        cells.sort()
        row_rank = [0] * rows
        col_rank = [0] * cols
        result = [[0] * cols for _ in range(rows)]
        i = 0
        while i < len(cells):
            j = i
            while j < len(cells) and cells[j][0] == cells[i][0]:
                j += 1
            # group of cells with same value
            parent: dict = {}

            def find(x):
                while parent.get(x, x) != x:
                    parent[x] = parent.get(parent[x], parent[x])
                    x = parent[x]
                return x

            for _, r, c in cells[i:j]:
                ru = ("r", r)
                cu = ("c", c)
                parent.setdefault(ru, ru)
                parent.setdefault(cu, cu)
                parent[find(ru)] = find(cu)
            buckets = defaultdict(list)
            for _, r, c in cells[i:j]:
                buckets[find(("r", r))].append((r, c))
            for group in buckets.values():
                rank = 1
                for r, c in group:
                    rank = max(rank, row_rank[r] + 1, col_rank[c] + 1)
                for r, c in group:
                    result[r][c] = rank
                    row_rank[r] = max(row_rank[r], rank)
                    col_rank[c] = max(col_rank[c], rank)
            i = j
        return result
