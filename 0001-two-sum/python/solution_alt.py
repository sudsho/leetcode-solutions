# alt approach: brute force O(n^2) version, kept for comparison

class Solution:
    def twoSum(self, nums, target):
        # brute force - O(n^2). keeping for reference
        n = len(nums)
        for i in range(n):
            for j in range(i+1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []
