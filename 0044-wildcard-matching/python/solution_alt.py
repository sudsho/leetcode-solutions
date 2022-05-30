# greedy two-pointer with star backtrack; O(1) extra space
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        i = j = 0
        star = -1
        si = 0
        while i < len(s):
            if j < len(p) and (p[j] == "?" or p[j] == s[i]):
                i += 1
                j += 1
            elif j < len(p) and p[j] == "*":
                star = j
                si = i
                j += 1
            elif star != -1:
                j = star + 1
                si += 1
                i = si
            else:
                return False
        while j < len(p) and p[j] == "*":
            j += 1
        return j == len(p)
