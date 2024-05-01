class Solution:
    def consecutiveNumbersSum(self, n: int) -> int:
        # 2n = k * (2a + k - 1); enumerate k
        n2 = 2 * n
        ways = 0
        k = 1
        while k * (k + 1) <= n2:
            if (n2 - k * (k - 1)) % (2 * k) == 0:
                ways += 1
            k += 1
        return ways
