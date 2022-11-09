# bfs-style queue version - simpler control flow
from typing import Tuple
from collections import deque

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
        seen = {(board, h0)}
        q = deque([(board, h0, 0)])
        while q:
            b, h, steps = q.popleft()
            if not b:
                return steps
            if not h:
                continue
            for i in range(len(b) + 1):
                for j in range(len(h)):
                    if j > 0 and h[j] == h[j - 1]:
                        continue
                    nb = collapse(b[:i] + h[j] + b[i:])
                    nh = h[:j] + h[j + 1:]
                    key = (nb, nh)
                    if key not in seen:
                        seen.add(key)
                        q.append((nb, nh, steps + 1))
        return -1
