from math import comb

class Solution:
    def numberOfWays(self, startPos: int, endPos: int, k: int) -> int:
        d = abs(endPos - startPos)
        if d > k or (k - d) & 1:
            return 0
        return comb(k, (k + d) // 2) % (10 ** 9 + 7)
