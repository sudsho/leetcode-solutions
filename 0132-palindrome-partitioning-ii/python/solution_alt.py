# 2023 nit (191)
# 1D dp using palindrome expansion around centers
class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        cuts = list(range(-1, n))
        for i in range(n):
            l = r = i
            while 0 <= l and r < n and s[l] == s[r]:
                cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
                l -= 1
                r += 1
            l, r = i, i + 1
            while 0 <= l and r < n and s[l] == s[r]:
                cuts[r + 1] = min(cuts[r + 1], cuts[l] + 1)
                l -= 1
                r += 1
        return cuts[n]
