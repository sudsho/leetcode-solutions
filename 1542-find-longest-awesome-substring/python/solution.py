class Solution:
    def longestAwesome(self, s: str) -> int:
        first = {0: -1}
        mask = 0
        best = 0
        for i, ch in enumerate(s):
            mask ^= 1 << int(ch)
            if mask in first:
                best = max(best, i - first[mask])
            else:
                first[mask] = i
            for k in range(10):
                m2 = mask ^ (1 << k)
                if m2 in first:
                    best = max(best, i - first[m2])
        return best
