from collections import deque

class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        # A* with h = number of mismatches // 2 (admissible)
        import heapq
        n = len(s1)
        if s1 == s2:
            return 0

        def heuristic(s: str) -> int:
            mis = sum(1 for a, b in zip(s, s2) if a != b)
            return (mis + 1) // 2
        heap: list[tuple[int, int, str]] = [(heuristic(s1), 0, s1)]
        seen: dict[str, int] = {s1: 0}
        while heap:
            f, g, cur = heapq.heappop(heap)
            if cur == s2:
                return g
            if seen.get(cur, 10 ** 9) < g:
                continue
            i = 0
            while cur[i] == s2[i]:
                i += 1
            for j in range(i + 1, n):
                if cur[j] == s2[i] and cur[j] != s2[j]:
                    nxt = cur[:i] + cur[j] + cur[i + 1:j] + cur[i] + cur[j + 1:]
                    ng = g + 1
                    if seen.get(nxt, 10 ** 9) > ng:
                        seen[nxt] = ng
                        heapq.heappush(heap, (ng + heuristic(nxt), ng, nxt))
        return -1
