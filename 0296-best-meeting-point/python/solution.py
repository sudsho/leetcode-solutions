class Solution:
    def minTotalDistance(self, grid):
        # manhattan distance separates into independent row and column costs,
        # so solve each 1-D problem and add them. the optimal meeting line in
        # 1-D sits at the median of the coordinates.
        rows = []
        cols = []
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == 1:
                    rows.append(r)
                    cols.append(c)
        # rows are collected in ascending order already; cols are not.
        cols.sort()
        return self._min_dist_1d(rows) + self._min_dist_1d(cols)

    def _min_dist_1d(self, coords):
        # sum of |x - median| minimized at the median. pairing the two
        # ends inward gives that total without naming the median: each pair
        # contributes its full span, since the median lies between them.
        total = 0
        i, j = 0, len(coords) - 1
        while i < j:
            total += coords[j] - coords[i]
            i += 1
            j -= 1
        return total
