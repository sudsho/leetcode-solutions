from typing import List
from sortedcontainers import SortedList

class Solution:
    def goodTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        pos = {v: i for i, v in enumerate(nums2)}
        a = [pos[v] for v in nums1]
        left = SortedList()
        right = SortedList(a[1:])
        ans = 0
        for i in range(n):
            # remove current from right
            if i > 0:
                right.remove(a[i])
            ls = left.bisect_left(a[i])
            rs = len(right) - right.bisect_right(a[i])
            ans += ls * rs
            left.add(a[i])
        return ans
