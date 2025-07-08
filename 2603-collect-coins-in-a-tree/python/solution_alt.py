from typing import List
from collections import defaultdict, deque

class Solution:
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)
        if n == 1:
            return 0
        adj: dict[int, set[int]] = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        # 1) trim leaves with coin == 0 iteratively
        q: deque[int] = deque(i for i in range(n) if len(adj[i]) == 1 and coins[i] == 0)
        while q:
            u = q.popleft()
            for v in list(adj[u]):
                adj[u].remove(v)
                adj[v].remove(u)
                if len(adj[v]) == 1 and coins[v] == 0:
                    q.append(v)
        # 2) trim two layers of leaves regardless of coin value
        leaves: deque[int] = deque(i for i in range(n) if len(adj[i]) == 1)
        for _ in range(2):
            sz = len(leaves)
            for _ in range(sz):
                u = leaves.popleft()
                for v in list(adj[u]):
                    adj[u].remove(v)
                    adj[v].remove(u)
                    if len(adj[v]) == 1:
                        leaves.append(v)
        # remaining edges; each visited twice
        rem_edges = sum(len(adj[i]) for i in range(n)) // 2
        return rem_edges * 2

# revisit: minor renames and one early exit added
