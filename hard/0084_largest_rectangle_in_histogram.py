# Given an array of integers heights representing the histogram's bar heights,
# find the area of the largest rectangle that can be formed within the histogram.
# Each bar has width 1. Use a monotonic stack to track candidate rectangles.

class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []  # stores indices of bars in increasing height order
        max_area = 0
        n = len(heights)

        for i in range(n + 1):
            # Use height 0 as sentinel to flush all remaining bars at the end
            current_height = heights[i] if i < n else 0

            while stack and heights[stack[-1]] > current_height:
                height = heights[stack.pop()]
                # Width extends from current position back to the new stack top
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)

            stack.append(i)

        return max_area


# Time complexity:  O(n) - each index pushed and popped at most once
# Space complexity: O(n) - stack can hold up to n elements


if __name__ == "__main__":
    sol = Solution()

    # Classic example: [2,1,5,6,2,3] → largest rectangle is 10 (bars 5,6 with width 2)
    assert sol.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10

    # Uniform heights: all bars same → full width × height
    assert sol.largestRectangleArea([3, 3, 3, 3]) == 12

    # Single bar
    assert sol.largestRectangleArea([7]) == 7

    print("All test cases passed.")
