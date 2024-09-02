class Solution:
    MOD = 10 ** 9 + 7

    def countPalindromicSubsequences(self, s: str) -> int:
        # Memoized recursion with letter-skipping to dedupe
        from functools import lru_cache
        n = len(s)

        @lru_cache(maxsize=None)
        def go(i: int, j: int) -> int:
            if i > j:
                return 0
            if i == j:
                return 1
            if s[i] != s[j]:
                return (go(i + 1, j) + go(i, j - 1) - go(i + 1, j - 1)) % self.MOD
            lo, hi = i + 1, j - 1
            while lo <= hi and s[lo] != s[i]:
                lo += 1
            while lo <= hi and s[hi] != s[i]:
                hi -= 1
            if lo > hi:
                return (2 * go(i + 1, j - 1) + 2) % self.MOD
            if lo == hi:
                return (2 * go(i + 1, j - 1) + 1) % self.MOD
            return (2 * go(i + 1, j - 1) - go(lo + 1, hi - 1)) % self.MOD
        return go(0, n - 1) % self.MOD
