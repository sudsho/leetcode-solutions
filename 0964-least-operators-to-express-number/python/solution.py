from functools import lru_cache

class Solution:
    def leastOpsExpressTarget(self, x: int, target: int) -> int:
        @lru_cache(maxsize=None)
        def go(t: int) -> int:
            if t == 0:
                return 0
            if t < x:
                # use t copies of (x/x)
                return min(t * 2 - 1, (x - t) * 2)
            k = 0
            v = 1
            while v * x <= t:
                v *= x
                k += 1
            if v == t:
                return k
            ans = go(t - v) + k
            if v * x - t < t - v:
                ans = min(ans, go(v * x - t) + k + 1)
            return ans
        return go(target)
# tightened naming
