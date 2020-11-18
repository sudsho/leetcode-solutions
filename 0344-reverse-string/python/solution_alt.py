# pythonic - reverse in place via slice trick
class Solution:
    def reverseString(self, s):
        s[:] = s[::-1]
