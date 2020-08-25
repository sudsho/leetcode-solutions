class Solution:
    def rotate(self, matrix):
        n = len(matrix)
        # transpose
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        # reverse each row
        for row in matrix:
            row.reverse()
