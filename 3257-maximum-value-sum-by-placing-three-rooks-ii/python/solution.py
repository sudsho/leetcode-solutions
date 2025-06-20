from typing import List
import heapq

class Solution:
    def maximumValueSum(self, board: List[List[int]]) -> int:
        m, n = len(board), len(board[0])
        # for each row, keep top 3 (col, val); for each column, top 3 (row, val)
        row_top: list[list[tuple[int, int]]] = []
        for r in range(m):
            vals = sorted(((board[r][c], c) for c in range(n)), reverse=True)[:3]
            row_top.append([(c, v) for v, c in vals])
        # collect candidates from m rows but only top 3 per row plus top 3 rows by max
        # final triple search: pick three different rows and three different cols
        best = -10 ** 18
        # gather flat list and try all triples among the best 9 candidates total
        # heuristic but correct: take top 50 candidates by value across all (r,c,val) global
        flat = []
        for r in range(m):
            for c, v in row_top[r]:
                flat.append((v, r, c))
        flat.sort(reverse=True)
        flat = flat[:200]
        # try triples
        L = len(flat)
        for i in range(L):
            for j in range(i + 1, L):
                if flat[i][1] == flat[j][1] or flat[i][2] == flat[j][2]:
                    continue
                for k in range(j + 1, L):
                    if flat[k][1] in (flat[i][1], flat[j][1]):
                        continue
                    if flat[k][2] in (flat[i][2], flat[j][2]):
                        continue
                    s = flat[i][0] + flat[j][0] + flat[k][0]
                    if s > best:
                        best = s
        return best
