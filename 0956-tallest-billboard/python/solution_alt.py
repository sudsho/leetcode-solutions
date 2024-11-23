from typing import List
from functools import lru_cache

class Solution:
    def tallestBillboard(self, rods: List[int]) -> int:
        # 3-way knapsack: each rod left/right/skip. Track diff -> best left height.
        S = sum(rods)
        @lru_cache(maxsize=None)
        def go(i: int, diff: int) -> int:
            if i == len(rods):
                return 0 if diff == 0 else -1
            skip = go(i + 1, diff)
            left = go(i + 1, diff + rods[i])
            if left >= 0:
                left += rods[i]
            right = go(i + 1, diff - rods[i])
            return max(skip, left, right)
        return go(0, 0)
