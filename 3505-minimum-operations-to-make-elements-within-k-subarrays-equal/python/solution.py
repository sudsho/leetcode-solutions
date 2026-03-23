from typing import List
from sortedcontainers import SortedList


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # cost[i] = min ops to make nums[i:i+x] all equal = sum |a - median| over window
        cost = [0] * (n - x + 1)
        sl_lo: SortedList[int] = SortedList()  # lower half
        sl_hi: SortedList[int] = SortedList()  # upper half
        sum_lo = 0
        sum_hi = 0

        def add(v: int):
            nonlocal sum_lo, sum_hi
            if not sl_lo or v <= sl_lo[-1]:
                sl_lo.add(v)
                sum_lo += v
            else:
                sl_hi.add(v)
                sum_hi += v
            balance()

        def remove(v: int):
            nonlocal sum_lo, sum_hi
            if v in sl_lo:
                sl_lo.remove(v)
                sum_lo -= v
            else:
                sl_hi.remove(v)
                sum_hi -= v
            balance()

        def balance():
            nonlocal sum_lo, sum_hi
            while len(sl_lo) > len(sl_hi) + 1:
                v = sl_lo.pop()
                sum_lo -= v
                sl_hi.add(v)
                sum_hi += v
            while len(sl_hi) > len(sl_lo):
                v = sl_hi.pop(0)
                sum_hi -= v
                sl_lo.add(v)
                sum_lo += v

        for i in range(x):
            add(nums[i])
        cost[0] = (sl_lo[-1] * len(sl_lo) - sum_lo) + (sum_hi - sl_lo[-1] * len(sl_hi))
        for i in range(1, n - x + 1):
            remove(nums[i - 1])
            add(nums[i + x - 1])
            cost[i] = (sl_lo[-1] * len(sl_lo) - sum_lo) + (sum_hi - sl_lo[-1] * len(sl_hi))
        # dp: pick k non-overlapping windows minimising sum of cost
        INF = 10**18
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        for i in range(n + 1):
            dp[0][i] = 0
        for j in range(1, k + 1):
            for i in range(j * x, n + 1):
                dp[j][i] = min(dp[j][i - 1], dp[j - 1][i - x] + cost[i - x])
        return dp[k][n]
