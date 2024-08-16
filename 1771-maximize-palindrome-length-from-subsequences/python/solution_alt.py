from functools import lru_cache

class Solution:
    def longestPalindrome(self, word1: str, word2: str) -> int:
        # Memoized recursion with explicit "must straddle" flag
        n1 = len(word1)
        s = word1 + word2

        @lru_cache(maxsize=None)
        def go(i: int, j: int, must: bool) -> int:
            if i > j:
                return -10 ** 9 if must else 0
            if i == j:
                return -10 ** 9 if must else 1
            if s[i] == s[j]:
                inner = go(i + 1, j - 1, must and not (i < n1 <= j))
                return inner + 2
            return max(go(i + 1, j, must), go(i, j - 1, must))
        return max(0, go(0, len(s) - 1, True))
