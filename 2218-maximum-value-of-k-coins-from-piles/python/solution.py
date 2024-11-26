from typing import List

class Solution:
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        dp = [0] * (k + 1)
        for pile in piles:
            new = dp[:]
            for j in range(1, k + 1):
                s = 0
                lim = min(j, len(pile))
                for t in range(lim):
                    s += pile[t]
                    if dp[j - t - 1] + s > new[j]:
                        new[j] = dp[j - t - 1] + s
            dp = new
        return dp[k]
# style tweak
