# alt: rolling hash check for longest palindromic prefix
class Solution:
    def shortestPalindrome(self, s: str) -> str:
        n = len(s)
        if n == 0:
            return s
        base, mod = 131, (1 << 61) - 1
        h1 = h2 = 0
        pw = 1
        best = 0
        for i, c in enumerate(s):
            v = ord(c)
            h1 = (h1 * base + v) % mod
            h2 = (h2 + v * pw) % mod
            pw = pw * base % mod
            if h1 == h2:
                best = i + 1
        return s[best:][::-1] + s
