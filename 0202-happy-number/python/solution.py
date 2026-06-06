class Solution:
    def isHappy(self, n):
        """A number is happy if repeatedly summing the squares of its digits
        eventually reaches 1. If it loops without hitting 1, it is not happy.
        Detect the cycle with Floyd's tortoise and hare so we use O(1) space."""

        def next_num(x):
            total = 0
            while x:
                x, d = divmod(x, 10)
                total += d * d
            return total

        slow = n
        fast = next_num(n)
        while fast != 1 and slow != fast:
            slow = next_num(slow)
            fast = next_num(next_num(fast))
        return fast == 1
