class Solution:
    def isIsomorphic(self, s, t):
        """Alternative: encode each string as the sequence of first-occurrence
        indices of its characters. Two strings are isomorphic iff these
        'shape' encodings match - identical structure regardless of the actual
        letters. One pass each, no two-way bookkeeping needed."""
        return self._pattern(s) == self._pattern(t)

    @staticmethod
    def _pattern(s):
        seen = {}
        out = []
        for ch in s:
            if ch not in seen:
                seen[ch] = len(seen)
            out.append(seen[ch])
        return out
