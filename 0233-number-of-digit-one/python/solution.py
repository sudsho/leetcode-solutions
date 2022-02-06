class Solution:
    def countDigitOne(self, n: int) -> int:
        if n <= 0:
            return 0
        m = 1
        total = 0
        while m <= n:
            divider = m * 10
            total += (n // divider) * m + min(max(n % divider - m + 1, 0), m)
            m = divider
        return total
