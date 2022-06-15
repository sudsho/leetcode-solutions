from typing import List
from sortedcontainers import SortedList

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        window = SortedList(nums[:k])
        out: List[float] = []
        mid_l = (k - 1) // 2
        mid_r = k // 2
        out.append((window[mid_l] + window[mid_r]) / 2)
        for i in range(k, len(nums)):
            window.remove(nums[i - k])
            window.add(nums[i])
            out.append((window[mid_l] + window[mid_r]) / 2)
        return out
