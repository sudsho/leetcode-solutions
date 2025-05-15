class Solution:
    def longestCommonSubsequence(self, t1: str, t2: str) -> int:
        if len(t1) < len(t2):
            t1, t2 = t2, t1
        prev = [0] * (len(t2) + 1)
        for c1 in t1:
            cur = [0] * (len(t2) + 1)
            for j, c2 in enumerate(t2, 1):
                if c1 == c2:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[-1]

# revisit: minor renames and one early exit added
