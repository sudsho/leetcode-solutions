from typing import List
from sortedcontainers import SortedList

class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int) -> int:
        d = [a - b for a, b in zip(nums1, nums2)]
        sl: SortedList[int] = SortedList()
        ans = 0
        for x in d:
            ans += sl.bisect_right(x + diff)
            sl.add(x)
        return ans
