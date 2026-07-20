class Solution:
    def wiggleMaxLength(self, nums):
        """Length of the longest wiggle subsequence.

        A wiggle sequence has strictly alternating up/down differences.
        Greedy: walk once, tracking the length of the best subsequence that
        currently ends on an "up" step and the best that ends on a "down" step.
        Each real rise can only extend the down-ending run (and vice versa),
        so counting the direction flips gives the answer.
        """
        if not nums:
            return 0
        up = down = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                up = down + 1
            elif nums[i] < nums[i-1]:
                down = up + 1
            # equal values contribute nothing; keep both runs as-is
        return max(up, down)
