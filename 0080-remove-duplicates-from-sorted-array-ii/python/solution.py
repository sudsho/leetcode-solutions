class Solution:
    def removeDuplicates(self, nums):
        # in-place, allow each value up to twice
        # write pointer k. for every n, only write if k < 2 or it differs
        # from the element two positions back. that enforces at-most-two.
        k = 0
        for n in nums:
            if k < 2 or n != nums[k - 2]:
                nums[k] = n
                k += 1
        return k
