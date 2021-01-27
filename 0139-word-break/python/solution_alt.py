# BFS variant
from collections import deque

class Solution:
    def wordBreak(self, s: str, wordDict) -> bool:
        words = set(wordDict)
        seen = set()
        q = deque([0])
        while q:
            i = q.popleft()
            if i == len(s):
                return True
            for j in range(i + 1, len(s) + 1):
                if j not in seen and s[i:j] in words:
                    seen.add(j)
                    q.append(j)
        return False
