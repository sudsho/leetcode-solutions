from typing import List

class Solution:
    def findPermutation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        INF = 10 ** 18
        # dp[mask][last] = (cost, previous tuple) reconstruct
        dp = [[INF] * n for _ in range(1 << n)]
        parent = [[-1] * n for _ in range(1 << n)]
        # start with 0 fixed
        dp[1][0] = 0
        for mask in range(1, 1 << n):
            if not (mask & 1):
                continue
            for last in range(n):
                if not (mask & (1 << last)):
                    continue
                if dp[mask][last] >= INF:
                    continue
                for nxt in range(n):
                    if mask & (1 << nxt):
                        continue
                    nm = mask | (1 << nxt)
                    cost = dp[mask][last] + abs(last - nums[nxt])
                    if cost < dp[nm][nxt]:
                        dp[nm][nxt] = cost
                        parent[nm][nxt] = last
        full = (1 << n) - 1
        # close: cost += |last - nums[0]|
        best_last = min(range(n), key=lambda x: dp[full][x] + abs(x - nums[0]))
        # reconstruct
        order: list[int] = []
        mask, cur = full, best_last
        while cur != -1:
            order.append(cur)
            prev = parent[mask][cur]
            mask ^= (1 << cur)
            cur = prev
        order.reverse()
        return order
