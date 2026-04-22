# Find the contiguous subarray with the largest product.
# Track both max and min at each step because two negatives multiply to a positive.

class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        cur_max = cur_min = result = nums[0]
        for n in nums[1:]:
            candidates = (n, cur_max * n, cur_min * n)
            cur_max, cur_min = max(candidates), min(candidates)
            result = max(result, cur_max)
        return result

# Time: O(n) | Space: O(1)

if __name__ == "__main__":
    sol = Solution()
    assert sol.maxProduct([2, 3, -2, 4]) == 6
    assert sol.maxProduct([-2, 0, -1]) == 0
    assert sol.maxProduct([-2, 3, -4]) == 24
    print("all tests passed")
