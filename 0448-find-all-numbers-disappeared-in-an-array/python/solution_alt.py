# alt approach: in-place sign-flipping trick. mutates input but uses O(1) extra space

class Solution:
    def findDisappearedNumbers(self, nums):
        # in-place sign flipping. O(1) extra space
        for n in nums:
            idx = abs(n) - 1
            if nums[idx] > 0:
                nums[idx] = -nums[idx]
        return [i + 1 for i, v in enumerate(nums) if v > 0]
