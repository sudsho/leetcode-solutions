# alt: scan with simple python list, no extra structure
from typing import List


class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        coins.sort()
        best = 0
        # forward sweep
        j = 0
        cur = 0
        for i in range(len(coins)):
            while j < len(coins) and coins[j][1] - coins[i][0] + 1 <= k:
                cur += (coins[j][1] - coins[j][0] + 1) * coins[j][2]
                j += 1
            if j < len(coins):
                # partial overlap on coins[j]
                end = coins[i][0] + k - 1
                if end >= coins[j][0]:
                    extra = (end - coins[j][0] + 1) * coins[j][2]
                    cand = cur + extra
                else:
                    cand = cur
            else:
                cand = cur
            if cand > best:
                best = cand
            cur -= (coins[i][1] - coins[i][0] + 1) * coins[i][2]
            # i moves past
        return best
