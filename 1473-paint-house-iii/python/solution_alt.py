from typing import List

class Solution:
    def minCost(self, houses: List[int], cost: List[List[int]], m: int, n: int, target: int) -> int:
        INF = float('inf')
        # dp[i][j][k] min cost up to i-th house, painted j, k neighborhoods used
        dp = [[[INF] * (target + 1) for _ in range(n + 1)] for _ in range(m + 1)]
        for j in range(1, n + 1):
            if houses[0] == 0 or houses[0] == j:
                add = 0 if houses[0] != 0 else cost[0][j - 1]
                dp[1][j][1] = add
        for i in range(2, m + 1):
            for j in range(1, n + 1):
                if houses[i - 1] != 0 and houses[i - 1] != j:
                    continue
                add = 0 if houses[i - 1] != 0 else cost[i - 1][j - 1]
                for k in range(1, target + 1):
                    best = dp[i - 1][j][k]
                    for jp in range(1, n + 1):
                        if jp != j:
                            if dp[i - 1][jp][k - 1] < best:
                                best = dp[i - 1][jp][k - 1]
                    if best < INF:
                        dp[i][j][k] = best + add
        ans = min(dp[m][j][target] for j in range(1, n + 1))
        return -1 if ans == INF else int(ans)

# revisit: minor renames and one early exit added
