class Solution:
    def generate(self, numRows):
        rows = []
        for i in range(numRows):
            row = [1] * (i + 1)
            for j in range(1, i):
                row[j] = rows[i - 1][j - 1] + rows[i - 1][j]
            rows.append(row)
        return rows
