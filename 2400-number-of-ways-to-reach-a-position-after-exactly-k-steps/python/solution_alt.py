from functools import cache

class Solution:
    def numberOfWays(self, startPos: int, endPos: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        d = abs(endPos - startPos)

        @cache
        def go(pos: int, left: int) -> int:
            if left == 0:
                return 1 if pos == d else 0
            if abs(pos - d) > left:
                return 0
            return (go(pos + 1, left - 1) + go(pos - 1, left - 1)) % MOD

        return go(0, k)
