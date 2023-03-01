from typing import List

class Trie:
    __slots__ = ('ch', 'word')
    def __init__(self):
        self.ch: dict[str, Trie] = {}
        self.word: str | None = None

class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = Trie()
        for w in words:
            node = root
            for c in w:
                node = node.ch.setdefault(c, Trie())
            node.word = w
        m, n = len(board), len(board[0])
        out: list[str] = []
        def dfs(i: int, j: int, node: Trie) -> None:
            ch = board[i][j]
            nxt = node.ch.get(ch)
            if not nxt:
                return
            if nxt.word is not None:
                out.append(nxt.word)
                nxt.word = None
            board[i][j] = '#'
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, nxt)
            board[i][j] = ch
            if not nxt.ch:
                node.ch.pop(ch, None)
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)
        return out
