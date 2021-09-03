from typing import List

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        INF = float("inf")
        cost = [INF] * n
        cost[src] = 0
        for _ in range(k + 1):
            new_cost = cost[:]
            for u, v, w in flights:
                if cost[u] + w < new_cost[v]:
                    new_cost[v] = cost[u] + w
            cost = new_cost
        return cost[dst] if cost[dst] != INF else -1
