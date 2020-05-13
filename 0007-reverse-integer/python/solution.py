# cleaned up
class Solution:
    def reverse(self, x):
        # handle sign separately
        sign = -1 if x < 0 else 1
        x = abs(x)

        result = 0
        while x > 0:
            result = result * 10 + x % 10
            x //= 10

        result = sign * result
        # 32 bit signed int range
        if result < -2**31 or result > 2**31 - 1:
            return 0
        return result
