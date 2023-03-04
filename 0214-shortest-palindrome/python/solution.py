class Solution:
    def shortestPalindrome(self, s: str) -> str:
        if not s:
            return s
        t = s + '#' + s[::-1]
        n = len(t)
        fail = [0] * n
        for i in range(1, n):
            j = fail[i - 1]
            while j > 0 and t[i] != t[j]:
                j = fail[j - 1]
            if t[i] == t[j]:
                j += 1
            fail[i] = j
        return s[fail[-1]:][::-1] + s
