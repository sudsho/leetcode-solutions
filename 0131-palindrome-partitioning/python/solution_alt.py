from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        out, cur = [], []

        def is_pal(a: int, b: int) -> bool:
            while a < b:
                if s[a] != s[b]:
                    return False
                a += 1; b -= 1
            return True

        def bt(i: int) -> None:
            if i == len(s):
                out.append(cur[:])
                return
            for j in range(i, len(s)):
                if is_pal(i, j):
                    cur.append(s[i:j + 1])
                    bt(j + 1)
                    cur.pop()

        bt(0)
        return out

# revisit: minor renames and one early exit added
