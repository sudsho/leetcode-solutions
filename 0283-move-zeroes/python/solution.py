class Solution:
    def moveZeroes(self, nums):
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
        # fill rest with zeros
        for i in range(slow, len(nums)):
            nums[i] = 0
