from typing import List

class Solution:
    def cheapestJump(self, coins: List[int], maxJump: int) -> List[int]:
        # Forward DP with greedy lex compare on path
        n = len(coins)
        if not coins or coins[-1] == -1 or coins[0] == -1:
            return []
        INF = float('inf')
        dp = [INF] * n
        dp[0] = coins[0]
        path: list[list[int]] = [[] for _ in range(n)]
        path[0] = [1]
        for i in range(1, n):
            if coins[i] == -1:
                continue
            for j in range(max(0, i - maxJump), i):
                if dp[j] == INF:
                    continue
                cand = dp[j] + coins[i]
                cand_path = path[j] + [i + 1]
                if cand < dp[i] or (cand == dp[i] and cand_path < path[i]):
                    dp[i] = cand
                    path[i] = cand_path
        return path[n - 1] if dp[n - 1] != INF else []
