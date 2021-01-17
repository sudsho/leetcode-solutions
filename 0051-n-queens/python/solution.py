from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        cols, d1, d2 = set(), set(), set()
        out = []
        placed = [-1] * n

        def bt(r: int) -> None:
            if r == n:
                out.append(["." * c + "Q" + "." * (n - c - 1) for c in placed])
                return
            for c in range(n):
                if c in cols or (r - c) in d1 or (r + c) in d2:
                    continue
                cols.add(c); d1.add(r - c); d2.add(r + c); placed[r] = c
                bt(r + 1)
                cols.remove(c); d1.remove(r - c); d2.remove(r + c)

        bt(0)
        return out
