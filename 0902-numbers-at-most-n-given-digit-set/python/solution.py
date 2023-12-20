from typing import List

class Solution:
    def atMostNGivenDigitSet(self, digits: List[str], n: int) -> int:
        s = str(n)
        L = len(s)
        K = len(digits)
        ans = 0
        for i in range(1, L):
            ans += K ** i
        for i, c in enumerate(s):
            smaller = sum(1 for d in digits if d < c)
            ans += smaller * (K ** (L - i - 1))
            if c not in digits:
                return ans
        return ans + 1
