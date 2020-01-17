# divide and conquer (overkill but interesting)
class Solution:
    def maxSubArray(self, nums):
        def go(l, r):
            if l == r:
                return nums[l]
            mid = (l + r) // 2
            left = go(l, mid)
            right = go(mid + 1, r)
            # cross
            cross_l = float("-inf")
            s = 0
            for i in range(mid, l - 1, -1):
                s += nums[i]
                cross_l = max(cross_l, s)
            cross_r = float("-inf")
            s = 0
            for i in range(mid + 1, r + 1):
                s += nums[i]
                cross_r = max(cross_r, s)
            return max(left, right, cross_l + cross_r)
        return go(0, len(nums) - 1)
