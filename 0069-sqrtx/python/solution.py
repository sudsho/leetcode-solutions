class Solution:
    def mySqrt(self, x: int) -> int:
        """Integer square root via binary search on the answer.

        Looking for the largest k with k*k <= x. Lower bound 0, upper bound x
        (safe for x in [0, 1] too). Compare k*k against x rather than dividing,
        since multiplication on Python ints is cheap and avoids the zero edge.
        """
        if x < 2:
            return x

        lo, hi = 1, x // 2 + 1
        best = 1
        while lo <= hi:
            mid = (lo + hi) // 2
            sq = mid * mid
            if sq == x:
                return mid
            if sq < x:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return best
