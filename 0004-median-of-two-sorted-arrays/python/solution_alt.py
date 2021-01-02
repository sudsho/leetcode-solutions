# brute O(m+n) merge approach for sanity check
from typing import List

class Solution:
    def findMedianSortedArrays(self, a: List[int], b: List[int]) -> float:
        merged = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i]); i += 1
            else:
                merged.append(b[j]); j += 1
        merged.extend(a[i:]); merged.extend(b[j:])
        n = len(merged)
        if n % 2:
            return float(merged[n // 2])
        return (merged[n // 2 - 1] + merged[n // 2]) / 2
