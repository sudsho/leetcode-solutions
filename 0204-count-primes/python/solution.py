class Solution:
    def countPrimes(self, n):
        # count primes strictly less than n with the sieve of eratosthenes
        if n < 3:
            return 0
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        # only need to sieve up to sqrt(n); any composite has a factor <= sqrt(n)
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                # start crossing out at i*i - smaller multiples already handled
                for j in range(i * i, n, i):
                    is_prime[j] = False
        return sum(is_prime)
