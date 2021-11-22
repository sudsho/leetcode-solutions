# revisit, tightened
class Solution:
    def countSubstrings(self, s):
        count = 0
        for i in range(len(s)):
            count += self._expand(s, i, i)
            count += self._expand(s, i, i + 1)
        return count

    def _expand(self, s, l, r):
        c = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            c += 1
            l -= 1
            r += 1
        return c
