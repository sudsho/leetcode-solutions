class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split()
        if len(words) != len(pattern):
            return False
        m1, m2 = {}, {}
        for ch, w in zip(pattern, words):
            if ch in m1 and m1[ch] != w:
                return False
            if w in m2 and m2[w] != ch:
                return False
            m1[ch] = w
            m2[w] = ch
        return True
