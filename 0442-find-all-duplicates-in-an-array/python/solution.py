class Solution:
    def findDuplicates(self, nums):
        """Find every value appearing twice in nums, O(1) extra space.

        Values are in [1, n], so each value v maps to index v-1. Walk the array
        and, for each value, flip the sign of the slot it points at. The first
        visit makes it negative; if we ever land on an already-negative slot the
        value that points there has been seen before, so record it.
        """
        out = []
        for x in nums:
            idx = abs(x) - 1
            if nums[idx] < 0:
                out.append(idx + 1)
            else:
                nums[idx] = -nums[idx]
        return out
