class Solution:
    def minWindow(self, s: str, t: str) -> str:
        n, m = len(s), len(t)
        i = 0
        best = ""
        while i < n:
            j = 0
            k = i
            while k < n and j < m:
                if s[k] == t[j]:
                    j += 1
                k += 1
            if j != m:
                break
            end = k
            k -= 1
            j = m - 1
            while j >= 0:
                if s[k] == t[j]:
                    j -= 1
                k -= 1
            k += 1
            if not best or end - k < len(best):
                best = s[k:end]
            i = k + 1
        return best
