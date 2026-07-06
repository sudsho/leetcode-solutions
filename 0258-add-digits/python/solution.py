class Solution:
    def addDigits(self, num):
        # keep folding the number into the sum of its digits until one digit remains
        while num >= 10:
            s = 0
            while num:
                s += num % 10
                num //= 10
            num = s
        return num
