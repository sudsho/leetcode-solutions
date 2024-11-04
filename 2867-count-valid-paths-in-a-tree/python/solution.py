from typing import List
from collections import defaultdict

class Solution:
    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        # union among composites
        parent = list(range(n + 1))
        size = [1] * (n + 1)
        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
        for u in range(1, n + 1):
            if sieve[u]:
                continue
            for v in graph[u]:
                if not sieve[v]:
                    union(u, v)
        ans = 0
        for p in range(2, n + 1):
            if not sieve[p]:
                continue
            sizes: list[int] = []
            total = 0
            for v in graph[p]:
                if not sieve[v]:
                    s = size[find(v)]
                    sizes.append(s)
                    total += s
            ans += total
            for s in sizes:
                ans += s * (total - s)
            ans //= 1
        # divide pair counting by 2
        return ans // 2
