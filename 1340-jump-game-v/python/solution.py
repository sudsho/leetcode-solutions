from functools import lru_cache
from typing import List

class Solution:
    def maxJumps(self, arr: List[int], d: int) -> int:
        n = len(arr)
        @lru_cache(maxsize=None)
        def go(i: int) -> int:
            best = 1
            for j in range(i - 1, max(-1, i - d - 1), -1):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + go(j))
            for j in range(i + 1, min(n, i + d + 1)):
                if arr[j] >= arr[i]:
                    break
                best = max(best, 1 + go(j))
            return best
        return max(go(i) for i in range(n))
# refactored helper
