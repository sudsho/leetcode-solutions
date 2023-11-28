from typing import List
from bisect import bisect_left

class Solution:
    def minimumMountainRemovals(self, nums: List[int]) -> int:
        def lis_lengths(arr):
            tails: list[int] = []
            res = []
            for x in arr:
                i = bisect_left(tails, x)
                if i == len(tails):
                    tails.append(x)
                else:
                    tails[i] = x
                res.append(i + 1)
            return res
        L = lis_lengths(nums)
        R = list(reversed(lis_lengths(list(reversed(nums)))))
        n = len(nums)
        best = 0
        for i in range(n):
            if L[i] >= 2 and R[i] >= 2:
                best = max(best, L[i] + R[i] - 1)
        return n - best
