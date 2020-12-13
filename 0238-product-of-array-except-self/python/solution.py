class Solution:
    def productExceptSelf(self, nums):
        n = len(nums)
        ans = [1] * n
        # prefix
        for i in range(1, n):
            ans[i] = ans[i - 1] * nums[i - 1]
        # suffix
        suf = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= suf
            suf *= nums[i]
        return ans
