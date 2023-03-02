# alt: dict-trie variant (slightly slower but simpler)
from typing import List

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root: dict = {}
        for w in words:
            node = root
            for c in w:
                node = node.setdefault(c, {})
            node['$'] = w
        m, n = len(board), len(board[0])
        out: list[str] = []
        def dfs(i, j, node):
            ch = board[i][j]
            if ch not in node:
                return
            nxt = node[ch]
            if '$' in nxt:
                out.append(nxt['$'])
                del nxt['$']
            board[i][j] = '#'
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, nxt)
            board[i][j] = ch
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)
        return out
