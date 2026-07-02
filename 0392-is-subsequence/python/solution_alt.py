import bisect
from collections import defaultdict


class Solution:
    def isSubsequence(self, s, t):
        """Follow-up: many queries s against the same t.

        Preprocess t once into, for each character, the sorted list of positions
        where it occurs. Then each query walks s and, tracking the last matched
        index in t, binary-searches for the next occurrence strictly after it.
        Preprocessing is O(len(t)); each query is O(len(s) * log len(t)), which
        beats re-scanning all of t per query.
        """
        positions = defaultdict(list)
        for i, ch in enumerate(t):
            positions[ch].append(i)

        prev = -1
        for ch in s:
            idx_list = positions.get(ch)
            if not idx_list:
                return False
            # First position of ch strictly greater than the last one we matched.
            j = bisect.bisect_right(idx_list, prev)
            if j == len(idx_list):
                return False
            prev = idx_list[j]
        return True
