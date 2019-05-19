class Solution:
    def maxSubArray(self, nums):
        # kadane's algorithm
        cur_sum = nums[0]
        best = nums[0]
        for x in nums[1:]:
            # either extend or restart
            cur_sum = max(x, cur_sum + x)
            best = max(best, cur_sum)
        return best
