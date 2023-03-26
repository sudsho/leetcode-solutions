from typing import List
from functools import lru_cache

class Solution:
    def removeBoxes(self, boxes: List[int]) -> int:
        n = len(boxes)
        @lru_cache(maxsize=None)
        def go(l: int, r: int, k: int) -> int:
            if l > r:
                return 0
            ll, kk = l, k
            while ll + 1 <= r and boxes[ll + 1] == boxes[ll]:
                ll += 1
                kk += 1
            best = (kk + 1) * (kk + 1) + go(ll + 1, r, 0)
            for m in range(ll + 1, r + 1):
                if boxes[m] == boxes[ll]:
                    best = max(best, go(ll + 1, m - 1, 0) + go(m, r, kk + 1))
            return best
        return go(0, n - 1, 0)
