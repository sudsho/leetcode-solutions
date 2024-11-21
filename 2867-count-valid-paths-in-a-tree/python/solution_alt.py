from typing import List
from collections import defaultdict

class Solution:
    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        # Simpler tree DP rooted at any prime, counting composite chains
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(n ** 0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False
        adj: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        ans = 0
        seen_root: dict[int, int] = {}

        def composite_size(start: int, banned: int) -> int:
            if start in seen_root:
                return seen_root[start]
            stack = [start]
            cnt = 0
            local_seen = {start, banned}
            while stack:
                u = stack.pop()
                cnt += 1
                for v in adj[u]:
                    if v in local_seen or is_prime[v]:
                        continue
                    local_seen.add(v)
                    stack.append(v)
            return cnt

        for p in range(2, n + 1):
            if not is_prime[p]:
                continue
            sizes: list[int] = []
            for v in adj[p]:
                if not is_prime[v]:
                    sizes.append(composite_size(v, p))
            total = sum(sizes)
            ans += total
            partial = 0
            for s in sizes:
                ans += s * partial
                partial += s
        return ans
