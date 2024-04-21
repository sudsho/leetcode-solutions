from functools import lru_cache

class Solution:
    def superEggDrop(self, k: int, n: int) -> int:
        @lru_cache(maxsize=None)
        def go(K: int, N: int) -> int:
            if K == 1:
                return N
            if N == 0:
                return 0
            lo, hi = 1, N
            while lo < hi:
                mid = (lo + hi) // 2
                broken = go(K - 1, mid - 1)
                survives = go(K, N - mid)
                if broken < survives:
                    lo = mid + 1
                else:
                    hi = mid
            return 1 + max(go(K - 1, lo - 1), go(K, N - lo))
        return go(k, n)
