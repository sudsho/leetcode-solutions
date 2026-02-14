from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # f[i] = set of OR values achievable from picking exactly j elems in nums[:i]
        # represent set of (j, value) as list of bitsets indexed by j
        def reachable(arr: List[int]) -> List[set[int]]:
            # dp[j] = set of OR values using j picks so far
            dp: list[set[int]] = [set() for _ in range(k + 1)]
            dp[0].add(0)
            for x in arr:
                for j in range(min(k, len(dp) - 1), 0, -1):
                    new = {v | x for v in dp[j - 1]}
                    dp[j] |= new
            return dp

        # at index i, prefix is nums[:i], suffix is nums[i:]
        # build prefix sets in forward sweep, suffix sets in reverse sweep
        pref: list[set[int]] = [set() for _ in range(n + 1)]
        pref[0].add(0)
        cur: list[set[int]] = [set() for _ in range(k + 1)]
        cur[0].add(0)
        # we need pref[i] = set of OR with exactly k picks from nums[:i]
        pref_k = [set() for _ in range(n + 1)]
        for i, x in enumerate(nums, 1):
            for j in range(min(k, i), 0, -1):
                cur[j] |= {v | x for v in cur[j - 1]}
            pref_k[i] = set(cur[k])
        suf: list[set[int]] = [set() for _ in range(k + 1)]
        suf[0].add(0)
        suf_k = [set() for _ in range(n + 2)]
        for i in range(n, 0, -1):
            x = nums[i - 1]
            for j in range(min(k, n - i + 1), 0, -1):
                suf[j] |= {v | x for v in suf[j - 1]}
            suf_k[i] = set(suf[k])
        best = 0
        for split in range(k, n - k + 1):
            a_set = pref_k[split]
            b_set = suf_k[split + 1]
            if not a_set or not b_set:
                continue
            for a in a_set:
                for b in b_set:
                    if (a ^ b) > best:
                        best = a ^ b
        return best
