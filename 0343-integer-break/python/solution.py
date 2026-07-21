class Solution:
    def integerBreak(self, n):
        """Break n into >= 2 positive parts to maximize their product.

        The math: past a point every factor should be a 3. A part of 4 ties with
        2+2, and any part >= 5 is beaten by peeling off a 3 (3*(k-3) > k for
        k >= 5), so an optimal split never uses a part bigger than 4 and prefers
        3 over 2. So use as many 3s as the total allows, then patch the remainder:
          - remainder 0: all 3s.
          - remainder 1: trade one 3 for a 4 (3+1 -> 2+2), since 3*1 < 2*2.
          - remainder 2: a single leftover 2.
        n = 2 and n = 3 are special because the "at least two parts" rule forces a
        1 into the split, capping them at 1 and 2.
        """
        if n <= 3:
            return n - 1  # 2 -> 1+1 = 1, 3 -> 1+2 = 2

        quotient, remainder = divmod(n, 3)
        if remainder == 0:
            return 3 ** quotient
        if remainder == 1:
            return 3 ** (quotient - 1) * 4
        return 3 ** quotient * 2
