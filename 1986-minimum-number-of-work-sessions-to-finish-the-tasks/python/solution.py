from typing import List
from functools import lru_cache

class Solution:
    def minSessions(self, tasks: List[int], sessionTime: int) -> int:
        n = len(tasks)
        full = (1 << n) - 1
        @lru_cache(maxsize=None)
        def go(mask: int, left: int) -> int:
            if mask == full:
                return 0
            best = 1 << 20
            for i in range(n):
                if mask >> i & 1:
                    continue
                if tasks[i] <= left:
                    best = min(best, go(mask | (1 << i), left - tasks[i]))
                else:
                    best = min(best, 1 + go(mask | (1 << i), sessionTime - tasks[i]))
            return best
        return 1 + go(0, 0)
