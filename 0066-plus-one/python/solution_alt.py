# alt approach: int-conversion version. easy but wasteful for huge inputs

class Solution:
    def plusOne(self, digits):
        # convert to int, add 1, convert back
        n = int(''.join(str(d) for d in digits)) + 1
        return [int(c) for c in str(n)]
