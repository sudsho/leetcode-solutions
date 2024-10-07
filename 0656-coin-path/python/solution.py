from typing import List

class Solution:
    def cheapestJump(self, coins: List[int], maxJump: int) -> List[int]:
        n = len(coins)
        if not coins or coins[-1] == -1:
            return []
        INF = float('inf')
        dp = [INF] * n
        nxt = [-1] * n
        dp[-1] = coins[-1]
        for i in range(n - 2, -1, -1):
            if coins[i] == -1:
                continue
            for j in range(i + 1, min(i + maxJump, n - 1) + 1):
                if dp[j] == INF:
                    continue
                if coins[i] + dp[j] < dp[i]:
                    dp[i] = coins[i] + dp[j]
                    nxt[i] = j
        if dp[0] == INF:
            return []
        path: list[int] = []
        i = 0
        while i != -1:
            path.append(i + 1)
            i = nxt[i]
        return path
