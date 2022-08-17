# bottom-up table
from typing import List

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        nums: List[int] = []
        ops: List[str] = []
        i = 0
        n = len(expression)
        while i < n:
            j = i
            while j < n and expression[j].isdigit():
                j += 1
            nums.append(int(expression[i:j]))
            if j < n:
                ops.append(expression[j])
            i = j + 1

        N = len(nums)
        dp: List[List[List[int]]] = [[[] for _ in range(N)] for _ in range(N)]
        for i in range(N):
            dp[i][i] = [nums[i]]
        for length in range(2, N + 1):
            for i in range(N - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    op = ops[k]
                    for a in dp[i][k]:
                        for b in dp[k + 1][j]:
                            if op == "+":
                                dp[i][j].append(a + b)
                            elif op == "-":
                                dp[i][j].append(a - b)
                            else:
                                dp[i][j].append(a * b)
        return dp[0][N - 1]
