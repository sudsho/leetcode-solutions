from functools import lru_cache

class Solution:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        @lru_cache(maxsize=None)
        def go(i: int, last: str, run: int, k: int) -> int:
            if k < 0:
                return 1 << 20
            if i == n:
                return 0
            best = 1 << 20
            # delete s[i]
            best = min(best, go(i + 1, last, run, k - 1))
            # keep s[i]
            if s[i] == last:
                inc = 1 if run in (1, 9, 99) else 0
                best = min(best, inc + go(i + 1, last, run + 1, k))
            else:
                best = min(best, 1 + go(i + 1, s[i], 1, k))
            return best
        return go(0, '', 0, k)
