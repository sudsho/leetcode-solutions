from typing import List

class Solution:
    def maxProfit(self, n: int, edges: List[List[int]], score: List[int]) -> int:
        prereq = [0] * n
        for a, b in edges:
            prereq[b] |= 1 << a
        full = (1 << n) - 1
        NEG = -10 ** 18
        dp = [NEG] * (1 << n)
        dp[0] = 0
        for mask in range(1 << n):
            if dp[mask] == NEG:
                continue
            depth = bin(mask).count('1') + 1
            for v in range(n):
                if mask & (1 << v):
                    continue
                if (prereq[v] & ~mask) != 0:
                    continue
                nm = mask | (1 << v)
                cand = dp[mask] + depth * score[v]
                if cand > dp[nm]:
                    dp[nm] = cand
        return dp[full]

# revisit: minor renames and one early exit added
