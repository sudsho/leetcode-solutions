from typing import List
from functools import lru_cache

class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        pts = sorted([0] + cuts + [n])
        m = len(pts)
        @lru_cache(maxsize=None)
        def go(i: int, j: int) -> int:
            if j - i <= 1:
                return 0
            return (pts[j] - pts[i]) + min(go(i, k) + go(k, j) for k in range(i + 1, j))
        return go(0, m - 1)
