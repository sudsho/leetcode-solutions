# string-form digit dp - reads cleaner for a refresh
from functools import lru_cache

class Solution:
    def countDigitOne(self, n: int) -> int:
        if n <= 0:
            return 0
        digits = list(map(int, str(n)))

        @lru_cache(maxsize=None)
        def dp(i: int, count: int, tight: bool) -> int:
            if i == len(digits):
                return count
            limit = digits[i] if tight else 9
            total = 0
            for d in range(limit + 1):
                total += dp(i + 1, count + (1 if d == 1 else 0), tight and d == limit)
            return total
        return dp(0, 0, True)
