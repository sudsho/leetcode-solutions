class Solution:
    def canJump(self, nums):
        """Greedily track the farthest index reachable so far.

        Sweep left to right keeping `farthest`, the highest index we can still
        get to. If the current index ever overtakes `farthest` there is a gap we
        cannot cross, so the last index is unreachable. Otherwise extend the
        reach by `i + nums[i]`. O(n) time, O(1) space.
        """
        farthest = 0
        for i, x in enumerate(nums):
            if i > farthest:
                return False
            if i + x > farthest:
                farthest = i + x
        return True
