# alt: O(1) digital-root formula, no looping
class Solution:
    def addDigits(self, num):
        # the repeated digit sum (digital root) cycles 1..9 for positive n,
        # so it's 0 when num is 0 and 1 + (num - 1) % 9 otherwise
        if num == 0:
            return 0
        return 1 + (num - 1) % 9
