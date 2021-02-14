from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""
        need = Counter(t)
        miss = len(t)
        l = best_l = 0
        best = float("inf")
        for r, c in enumerate(s):
            if need[c] > 0:
                miss -= 1
            need[c] -= 1
            while miss == 0:
                if r - l + 1 < best:
                    best = r - l + 1
                    best_l = l
                need[s[l]] += 1
                if need[s[l]] > 0:
                    miss += 1
                l += 1
        return "" if best == float("inf") else s[best_l:best_l + best]
