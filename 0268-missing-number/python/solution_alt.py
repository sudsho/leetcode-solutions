# revisited
class Solution:
    def missingNumber(self, nums):
        n = len(nums)
        expected = n * (n + 1) // 2
        return expected - sum(nums)

# revisit: minor renames and one early exit added
