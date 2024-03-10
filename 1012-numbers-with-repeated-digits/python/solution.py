class Solution:
    def numDupDigitsAtMostN(self, n: int) -> int:
        digits = list(map(int, str(n + 1)))
        L = len(digits)
        # count of numbers in [1,n] with all distinct digits
        unique = 0
        # length less than L
        prod = 9
        for i in range(1, L):
            unique += prod
            prod *= 10 - i
        # length == L
        seen: set[int] = set()
        for i, d in enumerate(digits):
            for x in range(0 if i else 1, d):
                if x in seen:
                    continue
                rem = 9 - i
                avail = rem
                p = 1
                for j in range(L - i - 1):
                    p *= avail
                    avail -= 1
                unique += p
            if d in seen:
                break
            seen.add(d)
        return n - unique
# tightened naming
