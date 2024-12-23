from typing import List
from functools import lru_cache

class Solution:
    def minimumFinishTime(self, tires: List[List[int]], changeTime: int, numLaps: int) -> int:
        # best_one[i] = min time to do i consecutive laps with same tire
        INF = 10 ** 18
        best_one = [INF] * 20
        for f, r in tires:
            t = f
            total = 0
            for k in range(1, 20):
                total += t
                if total >= INF:
                    break
                best_one[k] = min(best_one[k], total)
                t *= r
                if t > changeTime + f:
                    break
        @lru_cache(maxsize=None)
        def go(remaining: int) -> int:
            if remaining <= 0:
                return -changeTime  # offset because we add changeTime once at end
            best = INF
            for k in range(1, min(20, remaining + 1)):
                if best_one[k] >= INF:
                    continue
                best = min(best, best_one[k] + changeTime + go(remaining - k))
            return best
        return changeTime + go(numLaps)
# small fix
