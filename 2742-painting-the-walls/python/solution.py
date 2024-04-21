from typing import List
from functools import lru_cache

class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        n = len(cost)
        @lru_cache(maxsize=None)
        def go(i: int, remaining: int) -> int:
            if remaining <= 0:
                return 0
            if i == n:
                return 10 ** 9
            return min(
                cost[i] + go(i + 1, remaining - 1 - time[i]),
                go(i + 1, remaining),
            )
        return go(0, n)
