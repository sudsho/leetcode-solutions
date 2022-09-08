from math import factorial

class Solution:
    def getPermutation(self, n: int, k: int) -> str:
        digits = list(range(1, n + 1))
        k -= 1
        out = []
        for i in range(n, 0, -1):
            f = factorial(i - 1)
            idx = k // f
            out.append(str(digits.pop(idx)))
            k %= f
        return "".join(out)
# notes: simpler version above
# ok
