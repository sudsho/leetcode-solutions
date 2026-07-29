class Solution:
    def minSubarray(self, nums, p):
        n = len(nums)
        # the array total mod p is the debt we have to remove. if it is already
        # zero nothing needs deleting.
        target = sum(nums) % p
        if target == 0:
            return 0

        # we need the shortest subarray whose sum is congruent to target mod p,
        # i.e. prefix[i] - prefix[j] == target (mod p), which rearranges to
        #   prefix[j] == prefix[i] - target  (mod p)
        # so for each right end we look up that one specific earlier remainder.
        # this is the mirror of 974: there the wanted remainder was the current
        # one (difference 0), here it is shifted by the debt.
        last_seen = {0: -1}  # remainder -> LATEST index, because we want the shortest slice
        running = 0
        best = n
        for i, v in enumerate(nums):
            running = (running + v) % p
            want = (running - target) % p  # the % keeps it non-negative
            if want in last_seen:
                best = min(best, i - last_seen[want])
            # overwrite unconditionally: a later index with the same remainder
            # gives a shorter window for every future right end, so unlike 523
            # and 525 we keep the most recent one, not the first.
            last_seen[running] = i

        # deleting the whole array is not allowed, so a best of n means no valid
        # answer even though the arithmetic technically worked out.
        return best if best < n else -1
