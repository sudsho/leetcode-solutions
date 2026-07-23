# The guess API is provided by the judge:
#   def guess(num: int) -> int
#     returns -1 if my guess is too high, 1 if too low, 0 if correct.

class Solution:
    def guessNumber(self, n: int) -> int:
        """Binary search over [1, n]. Each call to guess() tells us which half
        the pick lives in, so we halve the range every step."""
        lo, hi = 1, n
        while lo <= hi:
            mid = lo + (hi - lo) // 2   # avoid overflow in other languages
            r = guess(mid)
            if r == 0:
                return mid
            if r < 0:          # mid too high, search the lower half
                hi = mid - 1
            else:              # mid too low, search the upper half
                lo = mid + 1
        return -1              # unreachable for a valid pick
