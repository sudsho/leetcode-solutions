from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        pre_n = [0] * (n + 1)
        pre_c = [0] * (n + 1)
        for i, (v, c) in enumerate(zip(nums, cost)):
            pre_n[i + 1] = pre_n[i] + v
            pre_c[i + 1] = pre_c[i] + c
        INF = 10 ** 18
        # dp[i][j] = min cost partitioning first i elements into j pieces
        # Often j is implicit; cost(l, r) = (pre_n[r] + j*k) * (pre_c[r] - pre_c[l-1])
        # We'll do O(n^2) DP for clarity (correct for moderate n)
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        for j in range(1, n + 1):
            for i in range(j, n + 1):
                # try breaking at l..i where last subarray is (l+1..i)
                best = INF
                for l in range(j - 1, i):
                    seg_n = pre_n[i] + j * k
                    seg_c = pre_c[i] - pre_c[l]
                    cand = dp[l][j - 1] + seg_n * seg_c
                    if cand < best:
                        best = cand
                dp[i][j] = best
        return min(dp[n][j] for j in range(1, n + 1))
