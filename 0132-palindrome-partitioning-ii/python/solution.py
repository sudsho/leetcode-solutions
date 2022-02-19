class Solution:
    def minCut(self, s: str) -> int:
        n = len(s)
        pal = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1):
                if s[i] == s[j] and (i - j < 2 or pal[j + 1][i - 1]):
                    pal[j][i] = True
        cuts = list(range(n))
        for i in range(n):
            if pal[0][i]:
                cuts[i] = 0
                continue
            for j in range(1, i + 1):
                if pal[j][i]:
                    cuts[i] = min(cuts[i], cuts[j - 1] + 1)
        return cuts[-1]
