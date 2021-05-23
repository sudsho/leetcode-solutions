# binary search on value, count <= mid in O(n)
from typing import List

class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)
        lo, hi = matrix[0][0], matrix[-1][-1]

        def count_le(x: int) -> int:
            cnt, c = 0, n - 1
            for r in range(n):
                while c >= 0 and matrix[r][c] > x:
                    c -= 1
                cnt += c + 1
            return cnt

        while lo < hi:
            mid = (lo + hi) // 2
            if count_le(mid) < k:
                lo = mid + 1
            else:
                hi = mid
        return lo
