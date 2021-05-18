from typing import List

class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        if len(a) > len(b):
            a, b = b, a
        m, n = len(a), len(b)
        half = (m + n + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2
            j = half - i
            al = a[i - 1] if i > 0 else float("-inf")
            ar = a[i] if i < m else float("inf")
            bl = b[j - 1] if j > 0 else float("-inf")
            br = b[j] if j < n else float("inf")
            if al <= br and bl <= ar:
                if (m + n) % 2:
                    return max(al, bl)
                return (max(al, bl) + min(ar, br)) / 2
            if al > br:
                hi = i - 1
            else:
                lo = i + 1
        return 0.0
# typing fix
