from collections import Counter
from functools import lru_cache

class Solution:
    def findMinStep(self, board: str, hand: str) -> int:
        def collapse(s: str) -> str:
            i = 0
            while i < len(s):
                j = i
                while j < len(s) and s[j] == s[i]:
                    j += 1
                if j - i >= 3:
                    return collapse(s[:i] + s[j:])
                i = j
            return s

        h0 = "".join(sorted(hand))
        seen: dict = {}

        def dfs(b: str, h: str) -> int:
            if not b:
                return 0
            if not h:
                return -1
            key = (b, h)
            if key in seen:
                return seen[key]
            best = -1
            for i in range(len(b) + 1):
                for j in range(len(h)):
                    if j > 0 and h[j] == h[j - 1]:
                        continue
                    if i > 0 and b[i - 1] == h[j]:
                        continue
                    if (i < len(b) and b[i] == h[j]) or (i > 0 and i < len(b) and b[i - 1] == b[i] and b[i] != h[j]):
                        nb = collapse(b[:i] + h[j] + b[i:])
                        nh = h[:j] + h[j + 1:]
                        sub = dfs(nb, nh)
                        if sub != -1:
                            cand = sub + 1
                            if best == -1 or cand < best:
                                best = cand
            seen[key] = best
            return best
        ans = dfs(board, h0)
        return ans
# notes: simpler version above
