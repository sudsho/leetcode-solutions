# bitmask version of solver - faster constant factor
from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        empty: List[tuple] = []
        for r in range(9):
            for c in range(9):
                v = board[r][c]
                if v == ".":
                    empty.append((r, c))
                else:
                    bit = 1 << (int(v) - 1)
                    rows[r] |= bit
                    cols[c] |= bit
                    boxes[(r // 3) * 3 + c // 3] |= bit

        def backtrack(i: int) -> bool:
            if i == len(empty):
                return True
            r, c = empty[i]
            b = (r // 3) * 3 + c // 3
            avail = (~(rows[r] | cols[c] | boxes[b])) & 0x1FF
            while avail:
                bit = avail & -avail
                avail ^= bit
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
                board[r][c] = str(bit.bit_length())
                if backtrack(i + 1):
                    return True
                rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
                board[r][c] = "."
            return False
        backtrack(0)
