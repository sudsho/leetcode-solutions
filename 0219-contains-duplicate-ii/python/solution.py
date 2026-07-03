class Solution:
    def containsNearbyDuplicate(self, nums, k):
        """True if some value repeats within a window of k indices.

        Keep a dict of value -> most recent index. When we see a value again,
        the closest prior occurrence is the one we stored, so checking that gap
        against k is enough; overwrite afterwards to keep the index fresh.
        """
        last_seen = {}
        for i, x in enumerate(nums):
            if x in last_seen and i - last_seen[x] <= k:
                return True
            last_seen[x] = i
        return False
