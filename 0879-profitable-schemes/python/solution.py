from typing import List

class Solution:
    MOD = 10 ** 9 + 7
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for g, p in zip(group, profit):
            new = [row[:] for row in dp]
            for j in range(n - g, -1, -1):
                for k in range(minProfit + 1):
                    new[j + g][min(minProfit, k + p)] = (
                        new[j + g][min(minProfit, k + p)] + dp[j][k]
                    ) % self.MOD
            dp = new
        return sum(dp[j][minProfit] for j in range(n + 1)) % self.MOD
# tightened naming
# style tweak
