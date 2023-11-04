# 2023 nit (180)
# bfs version - guarantees minimum-removal level
from typing import List
from collections import deque

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        def is_valid(t: str) -> bool:
            bal = 0
            for ch in t:
                if ch == "(":
                    bal += 1
                elif ch == ")":
                    bal -= 1
                if bal < 0:
                    return False
            return bal == 0

        seen = {s}
        q = deque([s])
        out: List[str] = []
        found = False
        while q:
            sz = len(q)
            for _ in range(sz):
                t = q.popleft()
                if is_valid(t):
                    out.append(t)
                    found = True
                if found:
                    continue
                for i, ch in enumerate(t):
                    if ch in "()":
                        nt = t[:i] + t[i + 1:]
                        if nt not in seen:
                            seen.add(nt)
                            q.append(nt)
            if found:
                break
        return out
