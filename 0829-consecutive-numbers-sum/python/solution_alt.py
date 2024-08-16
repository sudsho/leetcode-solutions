class Solution:
    def consecutiveNumbersSum(self, n: int) -> int:
        # Drop trailing 2s, count odd divisors
        while n % 2 == 0:
            n //= 2
        ways = 1
        d = 3
        while d * d <= n:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            ways *= cnt + 1
            d += 2
        if n > 1:
            ways *= 2
        return ways
