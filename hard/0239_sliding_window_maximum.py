# Given an array and window size k, return the max in each sliding window.
# Use a monotonic decreasing deque to track candidates in O(1) per step.

from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        dq = deque()   # stores indices; front is always the current window max
        result = []

        for i, val in enumerate(nums):
            # Remove indices outside the window
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            # Maintain decreasing order: drop smaller values from the back
            while dq and nums[dq[-1]] < val:
                dq.pop()
            dq.append(i)
            # Start recording once the first full window is reached
            if i >= k - 1:
                result.append(nums[dq[0]])

        return result

# Time: O(n) | Space: O(k)

if __name__ == "__main__":
    sol = Solution()
    assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sol.maxSlidingWindow([1], 1) == [1]
    assert sol.maxSlidingWindow([9, 8, 7, 6], 2) == [9, 8, 7]
    print("all tests passed")
