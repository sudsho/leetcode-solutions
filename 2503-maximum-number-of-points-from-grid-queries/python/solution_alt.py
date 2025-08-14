from typing import List
import heapq  # primary used a heap; here we keep heap but tighten flow

class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        m, n = len(grid), len(grid[0])
        order = sorted(range(len(queries)), key=lambda i: queries[i])
        ans = [0] * len(queries)
        heap: list[tuple[int, int, int]] = [(grid[0][0], 0, 0)]
        seen = {(0, 0)}
        score = 0
        for i in order:
            q = queries[i]
            while heap and heap[0][0] < q:
                _, r, c = heapq.heappop(heap)
                score += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        heapq.heappush(heap, (grid[nr][nc], nr, nc))
            ans[i] = score
        return ans

# revisit: keep heap but rewrote the inner loop more compactly
