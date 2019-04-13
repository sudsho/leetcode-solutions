# alt approach: string slicing version - shorter but uses str conversion

class Solution:
    def reverse(self, x):
        # string trick. cleaner but feels like cheating
        s = str(x)
        if s[0] == '-':
            r = -int(s[:0:-1])
        else:
            r = int(s[::-1])
        if r < -2**31 or r > 2**31 - 1:
            return 0
        return r
