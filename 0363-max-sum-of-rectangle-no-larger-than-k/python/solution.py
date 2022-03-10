from typing import List
from bisect import insort, bisect_left

class Solution:
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
        rows, cols = len(matrix), len(matrix[0])
        best = -float("inf")
        for r1 in range(rows):
            colsum = [0] * cols
            for r2 in range(r1, rows):
                for c in range(cols):
                    colsum[c] += matrix[r2][c]
                prefix = [0]
                cur = 0
                for x in colsum:
                    cur += x
                    i = bisect_left(prefix, cur - k)
                    if i < len(prefix):
                        best = max(best, cur - prefix[i])
                    insort(prefix, cur)
        return int(best)
