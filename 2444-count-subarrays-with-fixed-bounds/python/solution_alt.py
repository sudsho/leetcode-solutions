from typing import List

class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        # split on invalid then count within each window
        ans = 0
        i = 0
        n = len(nums)
        while i < n:
            j = i
            while j < n and minK <= nums[j] <= maxK:
                j += 1
            # process [i, j)
            mn = mx = -1
            for k in range(i, j):
                if nums[k] == minK:
                    mn = k
                if nums[k] == maxK:
                    mx = k
                if mn != -1 and mx != -1:
                    ans += min(mn, mx) - i + 1
            i = j + 1
        return ans
