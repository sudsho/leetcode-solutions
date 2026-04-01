# Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]]
# such that i != j != k and nums[i] + nums[j] + nums[k] == 0.
# Sort the array, fix one element, then use two pointers for the remaining pair.

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []

        for i in range(len(nums) - 2):
            # skip duplicates for the fixed element
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            # early exit: smallest possible sum already positive
            if nums[i] > 0:
                break

            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    # skip duplicates on both sides
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    right -= 1

        return result


# Time: O(n^2) — O(n log n) sort + O(n^2) two-pointer scan
# Space: O(1) extra (output list not counted)

if __name__ == "__main__":
    sol = Solution()
    print(sol.threeSum([-1, 0, 1, 2, -1, -4]))  # [[-1,-1,2],[-1,0,1]]
    print(sol.threeSum([0, 1, 1]))               # []
    print(sol.threeSum([0, 0, 0]))               # [[0,0,0]]
