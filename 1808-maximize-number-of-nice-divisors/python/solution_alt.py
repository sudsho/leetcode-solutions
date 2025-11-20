class Solution:
    def maxNiceDivisors(self, primeFactors: int) -> int:
        MOD = 10 ** 9 + 7
        if primeFactors <= 3:
            return primeFactors
        q, r = divmod(primeFactors, 3)
        if r == 0:
            return pow(3, q, MOD)
        if r == 1:
            return 4 * pow(3, q - 1, MOD) % MOD
        return 2 * pow(3, q, MOD) % MOD

# revisit: minor renames and one early exit added
