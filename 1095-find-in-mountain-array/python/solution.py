class MountainArray:
    def get(self, index: int) -> int: ...
    def length(self) -> int: ...

class Solution:
    def findInMountainArray(self, target: int, m: 'MountainArray') -> int:
        n = m.length()
        # find peak
        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if m.get(mid) < m.get(mid + 1):
                lo = mid + 1
            else:
                hi = mid
        peak = lo
        # left side ascending
        l, r = 0, peak
        while l <= r:
            mid = (l + r) // 2
            v = m.get(mid)
            if v == target:
                return mid
            if v < target:
                l = mid + 1
            else:
                r = mid - 1
        # right side descending
        l, r = peak, n - 1
        while l <= r:
            mid = (l + r) // 2
            v = m.get(mid)
            if v == target:
                return mid
            if v > target:
                l = mid + 1
            else:
                r = mid - 1
        return -1
