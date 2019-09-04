class Solution:
    def rob(self, nums):
        # prev2 = best up to two houses ago, prev1 = best up to last house
        prev2, prev1 = 0, 0
        for x in nums:
            prev2, prev1 = prev1, max(prev1, prev2 + x)
        return prev1
