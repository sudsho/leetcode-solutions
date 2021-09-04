from typing import List
from collections import defaultdict, deque

class Solution:
    def numBusesToDestination(self, routes: List[List[int]], source: int, target: int) -> int:
        if source == target:
            return 0
        stop_to_routes = defaultdict(set)
        for i, r in enumerate(routes):
            for s in r:
                stop_to_routes[s].add(i)
        visited_routes = set()
        visited_stops = {source}
        q = deque([(source, 0)])
        while q:
            stop, buses = q.popleft()
            for ri in stop_to_routes[stop]:
                if ri in visited_routes:
                    continue
                visited_routes.add(ri)
                for s in routes[ri]:
                    if s == target:
                        return buses + 1
                    if s not in visited_stops:
                        visited_stops.add(s)
                        q.append((s, buses + 1))
        return -1
