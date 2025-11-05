from typing import List

class Solution:
    def incremovableSubarrayCount(self, nums: List[int]) -> int:
        n = len(nums)
        l = 0
        while l + 1 < n and nums[l] < nums[l + 1]:
            l += 1
        if l == n - 1:
            return n * (n + 1) // 2
        r = n - 1
        while r > 0 and nums[r - 1] < nums[r]:
            r -= 1
        ans = (l + 1) + (n - r) * (l + 1)
        # for each i in [0,l], count j in [r,n-1] with nums[i] < nums[j]
        # we already counted (n - r) for i=-1 case in (l+1). Adjust:
        # restart cleanly:
        ans = (l + 2) + (n - r)
        # plus combinations between left prefix and right suffix
        i, j = 0, r
        # both ends inclusive
        while i <= l and j < n:
            while j < n and nums[j] <= nums[i]:
                j += 1
            ans += n - j
            i += 1
        return ans
