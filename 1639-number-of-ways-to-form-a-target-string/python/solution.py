from typing import List

class Solution:
    def numWays(self, words: List[str], target: str) -> int:
        MOD = 10 ** 9 + 7
        n = len(words[0])
        m = len(target)
        cnt = [[0] * 26 for _ in range(n)]
        for w in words:
            for j, c in enumerate(w):
                cnt[j][ord(c) - 97] += 1
        dp = [0] * (m + 1)
        dp[0] = 1
        for j in range(n):
            for i in range(min(j, m - 1), -1, -1):
                dp[i + 1] = (dp[i + 1] + dp[i] * cnt[j][ord(target[i]) - 97]) % MOD
        return dp[m]
