from typing import List
from collections import defaultdict
import sys

class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        sys.setrecursionlimit(10 ** 6)
        n = len(parent)
        children: dict[int, list[int]] = defaultdict(list)
        for i in range(1, n):
            children[parent[i]].append(i)
        for k in children:
            children[k].sort()
        order: list[str] = []
        start = [0] * n
        end = [0] * n

        def dfs(u: int) -> None:
            start[u] = len(order)
            for v in children[u]:
                dfs(v)
            order.append(s[u])
            end[u] = len(order)

        dfs(0)
        flat = ''.join(order)
        # Manacher on flat
        T = '#' + '#'.join(flat) + '#'
        L = len(T)
        p = [0] * L
        c = r = 0
        for i in range(L):
            mirror = 2 * c - i
            if i < r:
                p[i] = min(r - i, p[mirror])
            while i + p[i] + 1 < L and i - p[i] - 1 >= 0 and T[i + p[i] + 1] == T[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > r:
                c, r = i, i + p[i]

        ans = [False] * n
        for u in range(n):
            length = end[u] - start[u]
            center = start[u] + (end[u] - 1) - length // 2  # index in flat at center
            t_center = 2 * center + 1
            ans[u] = p[t_center] >= length
        return ans
