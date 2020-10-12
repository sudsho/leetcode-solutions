# write-pointer in place
class Solution:
    def moveZeroes(self, nums):
        w = 0
        for i in range(len(nums)):
            if nums[i] != 0:
                nums[w], nums[i] = nums[i], nums[w]
                w += 1
