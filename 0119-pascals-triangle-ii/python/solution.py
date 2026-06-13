class Solution:
    def getRow(self, rowIndex):
        """Return the rowIndex-th (0-indexed) row of Pascal's triangle.

        Build the row in place from the previous one. Each new row is the old
        row with a 1 appended, then every interior entry updated to the sum of
        the two above it. Walking right-to-left lets us overwrite in a single
        list without clobbering values we still need.
        """
        row = [1]
        for _ in range(rowIndex):
            row.append(1)
            for j in range(len(row) - 2, 0, -1):
                row[j] += row[j - 1]
        return row
