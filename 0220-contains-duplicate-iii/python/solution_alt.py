# alt: sortedcontainers SortedList window
from sortedcontainers import SortedList
from typing import List

class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        sl = SortedList()
        for i, x in enumerate(nums):
            pos = sl.bisect_left(x - valueDiff)
            if pos < len(sl) and sl[pos] <= x + valueDiff:
                return True
            sl.add(x)
            if len(sl) > indexDiff:
                sl.remove(nums[i - indexDiff])
        return False
