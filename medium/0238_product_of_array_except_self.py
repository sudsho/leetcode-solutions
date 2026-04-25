# Return an array where output[i] is the product of all elements except nums[i].
# Build prefix products left-to-right, then multiply suffix products right-to-left.

class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [1] * n

        # Forward pass: result[i] holds product of all elements to the left
        prefix = 1
        for i in range(n):
            result[i] = prefix
            prefix *= nums[i]

        # Backward pass: multiply in product of all elements to the right
        suffix = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix
            suffix *= nums[i]

        return result

# Time: O(n) | Space: O(1) extra (output array doesn't count)

if __name__ == "__main__":
    sol = Solution()
    assert sol.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert sol.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert sol.productExceptSelf([2, 3]) == [3, 2]
    print("all tests passed")
