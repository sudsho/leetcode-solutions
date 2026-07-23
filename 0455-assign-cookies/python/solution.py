class Solution:
    def findContentChildren(self, g, s):
        """Greedy two-pointer. Sort greed factors g and cookie sizes s ascending,
        then feed each child the smallest cookie that still satisfies them. Spending
        the smallest workable cookie keeps the larger ones for greedier children."""
        g.sort()
        s.sort()
        i = j = 0          # i -> child, j -> cookie
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:   # cookie j satisfies child i
                i += 1
            j += 1
        return i           # number of content children
