# simpler-to-read variant: maintain a Counter for the window and compare it to
# the target counter directly. clearer, but each comparison is O(26) so the
# constant factor is worse than the match-counting version in solution.py.
from collections import Counter
from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        m = len(p)
        if m > len(s):
            return []
        target = Counter(p)
        window = Counter(s[:m])
        out = [0] if window == target else []
        for i in range(m, len(s)):
            window[s[i]] += 1
            left = s[i - m]
            window[left] -= 1
            if window[left] == 0:
                del window[left]  # keep equality check honest
            if window == target:
                out.append(i - m + 1)
        return out
