from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # prefix[i] = sum of nums[:i]; subarray [l, r) has length r-l, sum prefix[r]-prefix[l]
        # we need (r - l) % k == 0, so l and r share same r % k bucket
        # for each bucket, track min prefix seen so far at indices with that mod
        best = -10**18
        min_pref_for_mod = [10**18] * k
        # i=0: prefix = 0, bucket = 0 % k
        min_pref_for_mod[0 % k] = 0
        s = 0
        for i in range(1, n + 1):
            s += nums[i - 1]
            b = i % k
            if min_pref_for_mod[b] < 10**18:
                cand = s - min_pref_for_mod[b]
                if cand > best:
                    best = cand
            if s < min_pref_for_mod[b]:
                min_pref_for_mod[b] = s
        return best
