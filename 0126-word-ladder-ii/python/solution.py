from collections import defaultdict, deque
from typing import List

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        words = set(wordList)
        if endWord not in words:
            return []
        layer = {beginWord}
        parents: dict[str, list[str]] = defaultdict(list)
        found = False
        while layer and not found:
            words -= layer
            nxt: set[str] = set()
            for w in layer:
                for i in range(len(w)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        nw = w[:i] + c + w[i + 1:]
                        if nw in words:
                            if nw == endWord:
                                found = True
                            nxt.add(nw)
                            parents[nw].append(w)
            layer = nxt

        out: list[list[str]] = []
        def back(node: str, path: list[str]) -> None:
            if node == beginWord:
                out.append([beginWord, *reversed(path)])
                return
            for p in parents[node]:
                path.append(node)
                back(p, path)
                path.pop()

        if found:
            back(endWord, [])
        return out
