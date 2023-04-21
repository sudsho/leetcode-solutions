class Solution:
    def preimageSizeFZF(self, k: int) -> int:
        def trailing_zeros(x: int) -> int:
            c = 0
            while x:
                x //= 5
                c += x
            return c
        def smallest(target: int) -> int:
            lo, hi = 0, 5 * (target + 1)
            while lo < hi:
                mid = (lo + hi) // 2
                if trailing_zeros(mid) >= target:
                    hi = mid
                else:
                    lo = mid + 1
            return lo
        return 5 if smallest(k + 1) - smallest(k) == 5 else 0
