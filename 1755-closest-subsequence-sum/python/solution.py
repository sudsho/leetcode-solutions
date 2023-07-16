from typing import List
from bisect import bisect_left

class Solution:
    def minAbsDifference(self, nums: List[int], goal: int) -> int:
        def sums(arr: List[int]) -> List[int]:
            out = [0]
            for x in arr:
                out += [s + x for s in out]
            return sorted(set(out))
        n = len(nums)
        L = sums(nums[:n // 2])
        R = sums(nums[n // 2:])
        best = abs(goal)
        for x in L:
            t = goal - x
            i = bisect_left(R, t)
            for j in (i - 1, i):
                if 0 <= j < len(R):
                    best = min(best, abs(goal - x - R[j]))
        return best
