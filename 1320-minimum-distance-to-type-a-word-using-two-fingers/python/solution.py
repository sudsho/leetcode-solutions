from functools import lru_cache

class Solution:
    def minimumDistance(self, word: str) -> int:
        def coord(c: str) -> tuple:
            i = ord(c) - ord("A")
            return divmod(i, 6)

        def cost(a, b) -> int:
            r1, c1 = coord(a)
            r2, c2 = coord(b)
            return abs(r1 - r2) + abs(c1 - c2)

        SENTINEL = "#"

        @lru_cache(maxsize=None)
        def dp(i: int, f1: str, f2: str) -> int:
            if i == len(word):
                return 0
            ch = word[i]
            move1 = (0 if f1 == SENTINEL else cost(f1, ch)) + dp(i + 1, ch, f2)
            move2 = (0 if f2 == SENTINEL else cost(f2, ch)) + dp(i + 1, f1, ch)
            return min(move1, move2)
        return dp(0, SENTINEL, SENTINEL)
