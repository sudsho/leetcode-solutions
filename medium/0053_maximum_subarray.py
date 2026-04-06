# Given an integer array nums, find the contiguous subarray with the largest sum.
# Classic dynamic programming problem using Kadane's algorithm.
# Return the maximum sum of any contiguous subarray.

class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        current_sum = nums[0]

        for num in nums[1:]:
            # either extend the current subarray or start fresh
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum


# Time Complexity: O(n) - single pass through the array
# Space Complexity: O(1) - only two variables maintained

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
    print(sol.maxSubArray([1]))                                # 1
    print(sol.maxSubArray([5, 4, -1, 7, 8]))                  # 23
