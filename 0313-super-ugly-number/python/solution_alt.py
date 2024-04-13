from typing import List

class Solution:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        # k-pointer dp variant
        k = len(primes)
        ugly = [1] * n
        idx = [0] * k
        for i in range(1, n):
            cand = min(primes[j] * ugly[idx[j]] for j in range(k))
            ugly[i] = cand
            for j in range(k):
                if primes[j] * ugly[idx[j]] == cand:
                    idx[j] += 1
        return ugly[n - 1]
