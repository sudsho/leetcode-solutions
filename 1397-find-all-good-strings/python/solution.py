class Solution:
    def findGoodStrings(self, n: int, s1: str, s2: str, evil: str) -> int:
        MOD = 10 ** 9 + 7
        m = len(evil)
        # kmp fail
        fail = [0] * m
        for i in range(1, m):
            j = fail[i - 1]
            while j > 0 and evil[i] != evil[j]:
                j = fail[j - 1]
            if evil[i] == evil[j]:
                j += 1
            fail[i] = j

        def trans(state: int, c: str) -> int:
            while state > 0 and (state == m or evil[state] != c):
                state = fail[state - 1]
            if state < m and evil[state] == c:
                state += 1
            return state

        from functools import lru_cache
        @lru_cache(maxsize=None)
        def go(i: int, state: int, low: bool, high: bool) -> int:
            if state == m:
                return 0
            if i == n:
                return 1
            lo = ord(s1[i]) if low else ord('a')
            hi = ord(s2[i]) if high else ord('z')
            total = 0
            for cc in range(lo, hi + 1):
                ch = chr(cc)
                ns = trans(state, ch)
                total = (total + go(i + 1, ns, low and cc == lo, high and cc == hi)) % MOD
            return total
        return go(0, 0, True, True)
