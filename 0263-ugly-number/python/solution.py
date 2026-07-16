class Solution:
    def isUgly(self, n):
        """An ugly number is positive and factors into only 2, 3, and 5.

        Divide out every 2, then every 3, then every 5. If what remains is 1,
        the number had no other prime factors and is ugly; anything else (or a
        non-positive input) is not. Each factor strips at least one bit/digit
        of magnitude, so the loops run O(log n) times total.
        """
        if n <= 0:
            return False
        for factor in (2, 3, 5):
            while n % factor == 0:
                n //= factor
        return n == 1
