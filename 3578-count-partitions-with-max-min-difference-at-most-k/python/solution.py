from typing import List
from collections import deque


class Solution:
    def countPartitions(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # dp[i] = number of ways to partition nums[:i]; dp[0] = 1
        # dp[i] = sum_{j: max(nums[j:i]) - min(nums[j:i]) <= k} dp[j]
        # for fixed i, valid j range is [L_i, i-1] where L_i is smallest j with window valid
        # use two monotonic deques to track max/min over [L, i-1] and a prefix-sum of dp
        dp = [0] * (n + 1)
        dp[0] = 1
        psum = [0] * (n + 2)  # psum[t] = sum dp[0..t-1]
        psum[1] = dp[0]
        max_dq: deque[int] = deque()
        min_dq: deque[int] = deque()
        L = 0
        for i in range(1, n + 1):
            # extend window to include index i-1
            x = nums[i - 1]
            while max_dq and nums[max_dq[-1]] <= x:
                max_dq.pop()
            max_dq.append(i - 1)
            while min_dq and nums[min_dq[-1]] >= x:
                min_dq.pop()
            min_dq.append(i - 1)
            # shrink from left until window valid
            while max_dq and min_dq and nums[max_dq[0]] - nums[min_dq[0]] > k:
                L += 1
                if max_dq[0] < L:
                    max_dq.popleft()
                if min_dq[0] < L:
                    min_dq.popleft()
            # dp[i] = sum dp[L..i-1] = psum[i] - psum[L]
            dp[i] = (psum[i] - psum[L]) % MOD
            psum[i + 1] = (psum[i] + dp[i]) % MOD
        return dp[n] % MOD
