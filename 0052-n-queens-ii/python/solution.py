class Solution:
    def totalNQueens(self, n):
        """Count distinct ways to place n non-attacking queens on an n x n board.
        Backtrack one row at a time, tracking occupied columns and both diagonal
        directions as sets so each placement check is O(1)."""
        cols = set()
        diag = set()      # r - c is constant along a "\" diagonal
        anti = set()      # r + c is constant along a "/" diagonal

        def backtrack(row):
            if row == n:
                return 1
            count = 0
            for col in range(n):
                if col in cols or (row - col) in diag or (row + col) in anti:
                    continue
                cols.add(col)
                diag.add(row - col)
                anti.add(row + col)
                count += backtrack(row + 1)
                cols.remove(col)
                diag.remove(row - col)
                anti.remove(row + col)
            return count

        return backtrack(0)
