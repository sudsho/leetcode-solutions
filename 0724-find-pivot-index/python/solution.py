class Solution:
    def pivotIndex(self, nums):
        # the pivot condition is left_sum == right_sum, and right_sum is fully
        # determined once we know the total and what is on the left:
        #   right = total - left - nums[i]
        # so a single running left sum answers the question at every index and
        # there is no need to materialize a prefix array at all.
        total = sum(nums)
        left = 0
        for i, v in enumerate(nums):
            # left is the sum strictly before i, so compare before absorbing v.
            if left == total - left - v:
                return i
            left += v
        return -1


class SolutionPrefix:
    """Explicit prefix array - same idea, kept for the shape it shares with 303."""

    def pivotIndex(self, nums):
        n = len(nums)
        # prefix[i] = sum of the first i elements, with the usual padding zero
        # at the front so prefix[i] is "everything strictly left of index i"
        # without a special case for i = 0.
        prefix = [0] * (n + 1)
        for i, v in enumerate(nums):
            prefix[i + 1] = prefix[i] + v
        for i in range(n):
            left = prefix[i]
            right = prefix[n] - prefix[i + 1]
            if left == right:
                return i
        return -1
