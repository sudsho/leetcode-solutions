from typing import List
from functools import lru_cache

class Solution:
    def minNumberOfSemesters(self, n: int, relations: List[List[int]], k: int) -> int:
        pre = [0] * n
        for a, b in relations:
            pre[b - 1] |= 1 << (a - 1)
        full = (1 << n) - 1

        @lru_cache(maxsize=None)
        def go(taken: int) -> int:
            if taken == full:
                return 0
            avail = 0
            for i in range(n):
                if not taken & (1 << i) and pre[i] & taken == pre[i]:
                    avail |= 1 << i
            best = 1 << 30
            sub = avail
            while sub > 0:
                if bin(sub).count('1') <= k:
                    best = min(best, 1 + go(taken | sub))
                sub = (sub - 1) & avail
            return best
        return go(0)
