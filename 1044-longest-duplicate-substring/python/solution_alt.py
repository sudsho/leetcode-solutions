# slower n^2 fallback used to sanity-check the rolling hash
class Solution:
    def longestDupSubstring(self, s: str) -> str:
        n = len(s)
        best = ""
        # quadratic approach: pivot on each starting index, build suffix array via sort
        suffixes = sorted(range(n), key=lambda i: s[i:])
        for i in range(1, n):
            a, b = suffixes[i - 1], suffixes[i]
            cap = min(n - a, n - b)
            j = 0
            while j < cap and s[a + j] == s[b + j]:
                j += 1
            if j > len(best):
                best = s[a:a + j]
        return best
