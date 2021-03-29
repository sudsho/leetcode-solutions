# iterative DP variant; lists each combo
from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]
        for c in candidates:
            for t in range(c, target + 1):
                for combo in dp[t - c]:
                    dp[t].append(combo + [c])
        return dp[target]
