# Given n non-negative integers representing elevation map where each bar has width 1,
# compute how much water it can trap after raining.
# Use two-pointer approach: track left/right max, fill water from smaller side inward.

class Solution:
    def trap(self, height: list[int]) -> int:
        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        water = 0

        while left < right:
            if height[left] <= height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]
                right -= 1

        return water

# Time: O(n) - single pass with two pointers
# Space: O(1) - only constant extra variables

if __name__ == "__main__":
    sol = Solution()
    print(sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6
    print(sol.trap([4, 2, 0, 3, 2, 5]))                      # 9
    print(sol.trap([3, 0, 2, 0, 4]))                          # 7
