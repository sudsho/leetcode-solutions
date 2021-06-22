class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        c1 = [0] * 26
        c2 = [0] * 26
        for ch in s1:
            c1[ord(ch) - 97] += 1
        for i, ch in enumerate(s2):
            c2[ord(ch) - 97] += 1
            if i >= len(s1):
                c2[ord(s2[i - len(s1)]) - 97] -= 1
            if c1 == c2:
                return True
        return False
