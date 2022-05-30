# bidirectional bfs, much faster on large dictionaries
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        words = set(wordList)
        if endWord not in words:
            return 0
        front, back = {beginWord}, {endWord}
        seen = set(front | back)
        steps = 1
        while front and back:
            steps += 1
            if len(front) > len(back):
                front, back = back, front
            nxt = set()
            for w in front:
                for i in range(len(w)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        nw = w[:i] + c + w[i + 1:]
                        if nw in back:
                            return steps
                        if nw in words and nw not in seen:
                            seen.add(nw)
                            nxt.add(nw)
            front = nxt
        return 0
