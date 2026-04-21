# Given an array nums of size n, return the majority element.
# The majority element appears more than n/2 times.
# Guaranteed to always exist in the array.

class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        # Boyer-Moore Voting Algorithm
        candidate = None
        count = 0
        for num in nums:
            if count == 0:
                candidate = num
            count += 1 if num == candidate else -1
        return candidate


# Time: O(n) - single pass through array
# Space: O(1) - only two variables

if __name__ == "__main__":
    sol = Solution()
    print(sol.majorityElement([3, 2, 3]))           # 3
    print(sol.majorityElement([2, 2, 1, 1, 1, 2, 2]))  # 2
    print(sol.majorityElement([1]))                  # 1
