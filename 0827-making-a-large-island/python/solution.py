class Solution:
    def largestIsland(self, grid):
        """Largest island after flipping at most one 0 to 1.

        Two passes. First, flood-fill every existing island and give it an id
        (starting at 2 so we don't collide with the 0/1 values) while recording
        its size. Then for every 0 cell, look at its four neighbours, collect the
        distinct island ids touching it, and the candidate size is 1 plus the sum
        of those islands' sizes. The answer is the best candidate, falling back to
        the largest existing island when the grid has no zeros.
        """
        n = len(grid)
        sizes = {}
        next_id = 2

        def fill(r, c, island_id):
            stack = [(r, c)]
            grid[r][c] = island_id
            count = 0
            while stack:
                x, y = stack.pop()
                count += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 1:
                        grid[nx][ny] = island_id
                        stack.append((nx, ny))
            return count

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    sizes[next_id] = fill(r, c, next_id)
                    next_id += 1

        # No flip needed yet: best is the largest island we already have.
        best = max(sizes.values(), default=0)

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    seen = set()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = r + dx, c + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] > 1:
                            seen.add(grid[nx][ny])
                    total = 1 + sum(sizes[i] for i in seen)
                    best = max(best, total)

        return best
