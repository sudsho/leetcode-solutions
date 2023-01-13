from functools import lru_cache

class Solution:
    def isScramble(self, s1: str, s2: str) -> bool:
        @lru_cache(maxsize=None)
        def go(a: str, b: str) -> bool:
            if a == b:
                return True
            if sorted(a) != sorted(b):
                return False
            n = len(a)
            for i in range(1, n):
                if go(a[:i], b[:i]) and go(a[i:], b[i:]):
                    return True
                if go(a[:i], b[-i:]) and go(a[i:], b[:-i]):
                    return True
            return False
        return go(s1, s2)
