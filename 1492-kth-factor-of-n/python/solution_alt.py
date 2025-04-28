class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        small = []
        large = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                small.append(i)
                if i != n // i:
                    large.append(n // i)
            i += 1
        factors = small + large[::-1]
        return factors[k - 1] if k <= len(factors) else -1

# revisit: minor renames and one early exit added
