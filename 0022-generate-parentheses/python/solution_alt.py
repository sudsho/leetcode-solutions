# iterative DP-style construction by length
from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        dp = [[""]]
        for i in range(1, n + 1):
            cur = []
            for j in range(i):
                for inside in dp[j]:
                    for outside in dp[i - 1 - j]:
                        cur.append("(" + inside + ")" + outside)
            dp.append(cur)
        return dp[n]
