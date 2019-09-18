# alt approach: sort-then-take-middle. O(n log n) but very short

class Solution:
    def majorityElement(self, nums):
        # sort and pick the middle
        # majority element is guaranteed to be at index n//2 after sort
        nums.sort()
        return nums[len(nums) // 2]
