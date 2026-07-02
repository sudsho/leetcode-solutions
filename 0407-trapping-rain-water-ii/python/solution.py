import heapq


class Solution:
    def trapRainWater(self, heightMap):
        """Volume of water trapped on a 2D elevation map.

        Water escapes over the lowest point of the outer wall, so process cells
        from the boundary inward, always expanding from the current lowest wall
        (a min-heap keyed on height). When we step to an unvisited neighbour, any
        gap between the wall level so far and that neighbour's floor holds water;
        the neighbour then joins the wall at max(wall, its own height), because
        water can never sit below the highest barrier already crossed.
        """
        if not heightMap or not heightMap[0]:
            return 0

        rows, cols = len(heightMap), len(heightMap[0])
        visited = [[False] * cols for _ in range(rows)]
        heap = []

        # Seed the heap with every border cell - water can only spill outward
        # across the outer ring, so that is where the enclosing walls start.
        for r in range(rows):
            for c in range(cols):
                if r in (0, rows - 1) or c in (0, cols - 1):
                    heapq.heappush(heap, (heightMap[r][c], r, c))
                    visited[r][c] = True

        trapped = 0
        while heap:
            wall, r, c = heapq.heappop(heap)
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                    visited[nr][nc] = True
                    trapped += max(0, wall - heightMap[nr][nc])
                    heapq.heappush(heap, (max(wall, heightMap[nr][nc]), nr, nc))
        return trapped
