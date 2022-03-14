# kadane fallback when number of cols >> rows
from typing import List
from bisect import bisect_left, insort

class Solution:
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
        rows, cols = len(matrix), len(matrix[0])
        if rows > cols:
            primary, secondary = rows, cols
            lookup = lambda i, j: matrix[i][j]
        else:
            primary, secondary = cols, rows
            lookup = lambda i, j: matrix[j][i]
        best = -float("inf")
        for i in range(primary):
            sums = [0] * secondary
            for j in range(i, primary):
                for s in range(secondary):
                    sums[s] += lookup(j, s)
                prefix = [0]
                cur = 0
                for x in sums:
                    cur += x
                    idx = bisect_left(prefix, cur - k)
                    if idx < len(prefix):
                        best = max(best, cur - prefix[idx])
                    insort(prefix, cur)
        return int(best)
