from math import comb


class Solution:
    def hasSameDigits(self, s: str) -> bool:
        # final pair = (sum_i C(n-2, i) * d_i mod 10, sum_i C(n-2, i) * d_{i+1} mod 10)
        # n is len(s); we reduce sequence n-2 times.
        n = len(s) - 2  # number of reductions when reducing to length 2
        if n < 0:
            # already len 2 or less
            return s[0] == s[1]
        # binomial mod 10 via CRT (mod 2 and mod 5 with Lucas).
        def lucas(n: int, k: int, p: int) -> int:
            res = 1
            while n > 0 or k > 0:
                a = n % p
                b = k % p
                if b > a:
                    return 0
                # C(a, b) mod p
                num = 1
                for i in range(b):
                    num = num * ((a - i) % p) % p
                den = 1
                for i in range(1, b + 1):
                    den = den * i % p
                # modular inverse mod p (prime): pow(den, p-2, p)
                res = res * num % p * pow(den, p - 2, p) % p
                n //= p
                k //= p
            return res

        def c_mod10(n: int, k: int) -> int:
            r2 = lucas(n, k, 2)
            r5 = lucas(n, k, 5)
            # CRT: x % 2 = r2, x % 5 = r5
            for x in range(10):
                if x % 2 == r2 and x % 5 == r5:
                    return x
            return 0

        digits = [int(c) for c in s]
        a = b = 0
        for i in range(len(digits) - 1):
            coef = c_mod10(n, i)
            a = (a + coef * digits[i]) % 10
            b = (b + coef * digits[i + 1]) % 10
        return a == b
