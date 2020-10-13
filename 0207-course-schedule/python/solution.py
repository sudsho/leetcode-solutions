from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses, prerequisites):
        graph = defaultdict(list)
        indeg = [0] * numCourses
        for a, b in prerequisites:
            graph[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        done = 0
        while q:
            x = q.popleft()
            done += 1
            for nb in graph[x]:
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    q.append(nb)
        return done == numCourses
