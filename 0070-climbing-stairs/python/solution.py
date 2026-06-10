class Solution:
    def climbStairs(self, n):
        """Ways to reach step n taking 1 or 2 steps at a time.

        The last move is either a single or a double step, so
        ways(n) = ways(n-1) + ways(n-2) - the Fibonacci recurrence. Roll two
        running values instead of a dp array to keep it O(1) space.
        """
        if n <= 2:
            return n
        # rolling fibonacci
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b
