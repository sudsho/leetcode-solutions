from typing import List
import heapq

class Solution:
    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        if m == n == 1:
            return 1
        row_heaps: list[list[tuple[int, int]]] = [[] for _ in range(m)]
        col_heaps: list[list[tuple[int, int]]] = [[] for _ in range(n)]
        # dist[i][j] = min cells visited to reach (i,j)
        # BFS by levels not strictly but a Dijkstra-like
        dist = [[-1] * n for _ in range(m)]
        dist[0][0] = 1
        q: list[tuple[int, int, int]] = [(1, 0, 0)]
        while q:
            d, i, j = heapq.heappop(q)
            if i == m - 1 and j == n - 1:
                return d
            if d > dist[i][j]:
                continue
            # push current cell to its row and col heaps
            heapq.heappush(row_heaps[i], (j, j + grid[i][j]))
            heapq.heappush(col_heaps[j], (i, i + grid[i][j]))
            # expand from current row
            while row_heaps[i] and row_heaps[i][0][0] <= j:
                jp, reach = heapq.heappop(row_heaps[i])
                if jp < j and reach >= j:
                    # not used
                    pass
            # this approach is heavy; do plain BFS along reachable
            # try next column candidates
            # we use lazy heaps differently: for each cell push (i, j) when visited
            # then expand to its reach
            limit_c = min(n - 1, j + grid[i][j])
            for jj in range(j + 1, limit_c + 1):
                if dist[i][jj] == -1:
                    dist[i][jj] = d + 1
                    heapq.heappush(q, (d + 1, i, jj))
            limit_r = min(m - 1, i + grid[i][j])
            for ii in range(i + 1, limit_r + 1):
                if dist[ii][j] == -1:
                    dist[ii][j] = d + 1
                    heapq.heappush(q, (d + 1, ii, j))
        return -1
