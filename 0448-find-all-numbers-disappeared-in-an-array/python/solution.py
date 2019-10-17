class Solution:
    def findDisappearedNumbers(self, nums):
        # set version - simpler. uses O(n) extra space
        present = set(nums)
        return [i for i in range(1, len(nums) + 1) if i not in present]
