# 2023 nit (73)
# build factoradic digits up front
from math import factorial

class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        nums = list(range(1, n + 1))
        k -= 1
        out = []
        facts = [factorial(i) for i in range(n)]
        for i in range(n - 1, -1, -1):
            idx, k = divmod(k, facts[i])
            out.append(str(nums.pop(idx)))
        return "".join(out)
