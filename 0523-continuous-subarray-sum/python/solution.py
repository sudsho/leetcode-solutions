class Solution:
    def checkSubarraySum(self, nums, k):
        # a subarray sums to a multiple of k exactly when its two enclosing
        # prefix sums leave the same remainder mod k, so the running value we
        # care about is the remainder rather than the sum itself.
        # first_seen[r] = earliest index whose prefix sum had remainder r.
        # remainder 0 sits at index -1 so a prefix that is already a multiple counts.
        first_seen = {0: -1}
        running = 0
        for i, v in enumerate(nums):
            running = (running + v) % k
            if running in first_seen:
                # the slice between the two matching remainders is a multiple of
                # k, but the problem wants length >= 2, so a neighbouring index
                # is not good enough.
                if i - first_seen[running] >= 2:
                    return True
            else:
                # keep only the FIRST index for a remainder - the earliest one
                # gives the widest window and so the best shot at clearing the
                # length-2 floor. overwriting would quietly reject valid cases.
                first_seen[running] = i
        return False
