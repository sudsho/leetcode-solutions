class Solution:
    def findDisappearedNumbers(self, nums):
        """Return the values in [1, n] that never appear in nums.

        Set version - simplest to read, uses O(n) extra space. The values are in
        [1, n], so the same index-as-hash sign-marking trick used for 442 gives
        an O(1)-space alternative if needed.
        """
        present = set(nums)
        return [i for i in range(1, len(nums) + 1) if i not in present]
