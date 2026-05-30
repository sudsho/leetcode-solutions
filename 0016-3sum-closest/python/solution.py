from typing import List


class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """Find three numbers whose sum is closest to target.

        Sort, then for each anchor i sweep two pointers from both ends. Same
        shape as 3Sum but we track the running best by |sum - target| instead
        of looking for zero. Early-exit on exact hit since you can't beat 0.
        """
        nums.sort()
        n = len(nums)
        best = nums[0] + nums[1] + nums[2]

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s == target:
                    return s
                if abs(s - target) < abs(best - target):
                    best = s
                if s < target:
                    lo += 1
                else:
                    hi -= 1
        return best
