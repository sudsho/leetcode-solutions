from collections import deque

class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        if s1 == s2:
            return 0
        seen = {s1}
        q: deque[tuple[str, int]] = deque([(s1, 0)])
        while q:
            cur, d = q.popleft()
            i = 0
            while cur[i] == s2[i]:
                i += 1
            for j in range(i + 1, len(cur)):
                if cur[j] == s2[i] and cur[j] != s2[j]:
                    nxt = cur[:i] + cur[j] + cur[i + 1:j] + cur[i] + cur[j + 1:]
                    if nxt == s2:
                        return d + 1
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, d + 1))
        return -1
