# Given n vertical lines where heights[i] is the height of line i,
# find two lines that together with the x-axis forms a container
# that holds the most water.

class Solution:
    def maxArea(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        max_water = 0

        while left < right:
            width = right - left
            water = width * min(height[left], height[right])
            max_water = max(max_water, water)

            # move the pointer with the shorter line inward
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water


# Time Complexity: O(n) - single pass with two pointers
# Space Complexity: O(1) - constant extra space


if __name__ == "__main__":
    sol = Solution()

    # Example 1: [1,8,6,2,5,4,8,3,7] -> 49 (lines at index 1 and 8)
    print(sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49

    # Example 2: [1,1] -> 1
    print(sol.maxArea([1, 1]))  # 1

    # Example 3: [4,3,2,1,4] -> 16 (lines at index 0 and 4)
    print(sol.maxArea([4, 3, 2, 1, 4]))  # 16
