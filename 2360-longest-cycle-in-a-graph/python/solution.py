from typing import List

class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        visit_time = [-1] * n
        finished = [False] * n
        ans = -1
        timer = 0
        for start in range(n):
            if finished[start]:
                continue
            local_start = timer
            u = start
            while u != -1 and not finished[u]:
                if visit_time[u] != -1:
                    if visit_time[u] >= local_start:
                        ans = max(ans, timer - visit_time[u])
                    break
                visit_time[u] = timer
                timer += 1
                u = edges[u]
            # mark all visited in this walk as finished
            v = start
            while v != -1 and not finished[v]:
                finished[v] = True
                v = edges[v]
        return ans
