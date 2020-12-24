# memoized recursion
class Solution:
    def fib(self, n):
        memo = {0: 0, 1: 1}
        def go(k):
            if k in memo:
                return memo[k]
            memo[k] = go(k - 1) + go(k - 2)
            return memo[k]
        return go(n)
