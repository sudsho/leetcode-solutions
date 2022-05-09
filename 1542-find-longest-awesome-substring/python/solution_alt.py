# alt with default-dict for first-seen positions
from collections import defaultdict

class Solution:
    def longestAwesome(self, s: str) -> int:
        first = defaultdict(lambda: -2)
        first[0] = -1
        mask = 0
        best = 0
        for i, ch in enumerate(s):
            mask ^= 1 << (ord(ch) - ord("0"))
            if first[mask] != -2:
                best = max(best, i - first[mask])
            else:
                first[mask] = i
            for k in range(10):
                m2 = mask ^ (1 << k)
                if first[m2] != -2:
                    best = max(best, i - first[m2])
        return best
