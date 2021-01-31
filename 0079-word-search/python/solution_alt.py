# alt: recursive with explicit visited set
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m, n = len(board), len(board[0])
        seen = set()

        def dfs(r: int, c: int, k: int) -> bool:
            if k == len(word):
                return True
            if r < 0 or r >= m or c < 0 or c >= n:
                return False
            if (r, c) in seen or board[r][c] != word[k]:
                return False
            seen.add((r, c))
            ok = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                  or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
            seen.remove((r, c))
            return ok

        return any(dfs(r, c, 0) for r in range(m) for c in range(n))
