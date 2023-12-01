# alt: revisited in 2023, slight cleanup
from typing import List, Optional

# original idea kept; this version uses match/dataclass-style refactor where it helps.

from typing import List
from collections import defaultdict
import heapq

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        for a, b in tickets:
            heapq.heappush(graph[a], b)
        route: List[str] = []

        def dfs(u: str) -> None:
            while graph[u]:
                v = heapq.heappop(graph[u])
                dfs(v)
            route.append(u)

        dfs("JFK")
        return route[::-1]
