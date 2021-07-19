# small cleanup
class Solution:
    def canPartition(self, nums):
        s = sum(nums)
        if s % 2:
            return False
        target = s // 2
        dp = [False] * (target + 1)
        dp[0] = True
        for n in nums:
            for t in range(target, n - 1, -1):
                dp[t] = dp[t] or dp[t - n]
            if dp[target]:
                return True
        return dp[target]
