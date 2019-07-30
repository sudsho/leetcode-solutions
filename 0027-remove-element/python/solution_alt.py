# alt approach: swap-with-last variant. fewer copies when val is rare

class Solution:
    def removeElement(self, nums, val):
        # swap-with-end version - good when val is rare
        i = 0
        n = len(nums)
        while i < n:
            if nums[i] == val:
                nums[i] = nums[n-1]
                n -= 1
            else:
                i += 1
        return n
