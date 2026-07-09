class NumMatrix:
    """2D range-sum with point updates backed by a 2D Binary Indexed Tree.

    A Fenwick tree gives O(log m * log n) updates and prefix-rectangle queries.
    The rectangle sum (r1,c1)..(r2,c2) comes from inclusion-exclusion over four
    prefix sums, exactly like the 1D prefix-sum trick lifted to two dimensions.
    """

    def __init__(self, matrix):
        if not matrix or not matrix[0]:
            self.rows = self.cols = 0
            return
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        # tree is 1-indexed on both axes; nums keeps the current cell values so
        # update() can compute the delta to push into the tree.
        self.nums = [[0] * self.cols for _ in range(self.rows)]
        self.tree = [[0] * (self.cols + 1) for _ in range(self.rows + 1)]
        for r in range(self.rows):
            for c in range(self.cols):
                self.update(r, c, matrix[r][c])

    def update(self, row, col, val):
        if self.rows == 0:
            return
        delta = val - self.nums[row][col]
        self.nums[row][col] = val
        i = row + 1
        while i <= self.rows:
            j = col + 1
            while j <= self.cols:
                self.tree[i][j] += delta
                j += j & (-j)
            i += i & (-i)

    def _prefix(self, row, col):
        """Sum of the rectangle from (0,0) to (row-1, col-1) inclusive."""
        total = 0
        i = row
        while i > 0:
            j = col
            while j > 0:
                total += self.tree[i][j]
                j -= j & (-j)
            i -= i & (-i)
        return total

    def sumRegion(self, row1, col1, row2, col2):
        if self.rows == 0:
            return 0
        return (
            self._prefix(row2 + 1, col2 + 1)
            - self._prefix(row1, col2 + 1)
            - self._prefix(row2 + 1, col1)
            + self._prefix(row1, col1)
        )
