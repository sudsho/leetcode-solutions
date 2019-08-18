class Solution:
    def singleNumber(self, nums):
        # x ^ x = 0, x ^ 0 = x, so all duplicates cancel
        out = 0
        for n in nums:
            out ^= n
        return out
