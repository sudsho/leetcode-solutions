from typing import List
from functools import lru_cache

class Solution:
    MOD = 10 ** 9 + 7
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        L = len(group)
        @lru_cache(maxsize=None)
        def go(i: int, people: int, prof: int) -> int:
            if i == L:
                return 1 if prof >= minProfit else 0
            res = go(i + 1, people, prof)
            if people + group[i] <= n:
                res += go(i + 1, people + group[i], min(minProfit, prof + profit[i]))
            return res % self.MOD
        return go(0, 0, 0)
