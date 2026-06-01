# cleaned up
class Solution:
    def removeElement(self, nums, val):
        """In-place removal of val; returns the new length."""
        write = 0
        for read in range(len(nums)):
            if nums[read] != val:
                nums[write] = nums[read]
                write += 1
        return write
