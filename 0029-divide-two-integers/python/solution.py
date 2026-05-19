class Solution:
    def divide(self, dividend, divisor):
        # 32-bit signed clamp range
        INT_MAX = 2**31 - 1
        INT_MIN = -(2**31)

        # only overflow case in 32-bit signed division
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        negative = (dividend < 0) ^ (divisor < 0)
        a = abs(dividend)
        b = abs(divisor)

        # subtract the largest doubled multiple of b that still fits, repeat
        result = 0
        while a >= b:
            shift = 0
            while a >= (b << (shift + 1)):
                shift += 1
            a -= b << shift
            result += 1 << shift

        if negative:
            result = -result
        if result > INT_MAX:
            return INT_MAX
        if result < INT_MIN:
            return INT_MIN
        return result


if __name__ == "__main__":
    sol = Solution()
    print(sol.divide(10, 3))
    print(sol.divide(7, -3))
    print(sol.divide(-2147483648, -1))
    print(sol.divide(-2147483648, 1))
    print(sol.divide(0, 1))
