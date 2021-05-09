# walk from right, jumping with current next-warmer indices
from typing import List

class Solution:
    def dailyTemperatures(self, temps: List[int]) -> List[int]:
        n = len(temps)
        res = [0] * n
        for i in range(n - 2, -1, -1):
            j = i + 1
            while j < n and temps[j] <= temps[i]:
                if res[j] == 0:
                    j = n
                    break
                j += res[j]
            if j < n:
                res[i] = j - i
        return res
