from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empty: List[tuple] = []
        for r in range(9):
            for c in range(9):
                v = board[r][c]
                if v == ".":
                    empty.append((r, c))
                else:
                    rows[r].add(v)
                    cols[c].add(v)
                    boxes[(r // 3) * 3 + c // 3].add(v)

        def backtrack(i: int) -> bool:
            if i == len(empty):
                return True
            r, c = empty[i]
            b = (r // 3) * 3 + c // 3
            for d in "123456789":
                if d not in rows[r] and d not in cols[c] and d not in boxes[b]:
                    rows[r].add(d); cols[c].add(d); boxes[b].add(d)
                    board[r][c] = d
                    if backtrack(i + 1):
                        return True
                    rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)
                    board[r][c] = "."
            return False

        backtrack(0)
# follow up: revisit if profiling cares
# revised after retry
