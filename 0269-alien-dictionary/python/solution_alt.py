# 2023 nit (136)
# dfs based topological sort
from typing import List
from collections import defaultdict

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = defaultdict(set)
        seen = {ch for w in words for ch in w}
        for a, b in zip(words, words[1:]):
            for x, y in zip(a, b):
                if x != y:
                    graph[x].add(y)
                    break
            else:
                if len(b) < len(a):
                    return ""
        order = []
        state = {}
        cycle = False

        def dfs(c: str) -> None:
            nonlocal cycle
            if cycle:
                return
            if state.get(c) == 1:
                cycle = True
                return
            if state.get(c) == 2:
                return
            state[c] = 1
            for nb in graph[c]:
                dfs(nb)
            state[c] = 2
            order.append(c)

        for c in seen:
            if c not in state:
                dfs(c)
        if cycle:
            return ""
        return "".join(reversed(order))
