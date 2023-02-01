# alt: bidirectional bfs, then reconstruct
from collections import defaultdict
from typing import List

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        words = set(wordList)
        if endWord not in words:
            return []
        front, back = {beginWord}, {endWord}
        graph: dict[str, set[str]] = defaultdict(set)
        rev = False
        found = False
        while front and back and not found:
            if len(front) > len(back):
                front, back = back, front
                rev = not rev
            words -= front
            nxt: set[str] = set()
            for w in front:
                for i in range(len(w)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        nw = w[:i] + c + w[i + 1:]
                        if nw in words or nw in back:
                            if nw in back:
                                found = True
                            if rev:
                                graph[nw].add(w)
                            else:
                                graph[w].add(nw)
                            if nw not in back:
                                nxt.add(nw)
            front = nxt

        out: list[list[str]] = []
        def dfs(w: str, path: list[str]) -> None:
            if w == endWord:
                out.append(path[:])
                return
            for nb in graph[w]:
                path.append(nb)
                dfs(nb, path)
                path.pop()
        dfs(beginWord, [beginWord])
        return out
