# alt: simple per-node check with explicit string build (slow but correct)
from typing import List
from collections import defaultdict


class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        children = defaultdict(list)
        for v in range(1, n):
            children[parent[v]].append(v)
        for k in children:
            children[k].sort()

        def build(u: int) -> str:
            parts = [build(c) for c in children[u]]
            return "".join(parts) + s[u]

        out = []
        for u in range(n):
            t = build(u)
            out.append(t == t[::-1])
        return out
