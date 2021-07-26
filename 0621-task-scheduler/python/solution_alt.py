# heap simulation variant
from collections import Counter, deque
from typing import List
import heapq

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        h = [-c for c in Counter(tasks).values()]
        heapq.heapify(h)
        time = 0
        q = deque()  # (count, ready_time)
        while h or q:
            time += 1
            if h:
                cnt = heapq.heappop(h) + 1
                if cnt < 0:
                    q.append((cnt, time + n))
            if q and q[0][1] == time:
                heapq.heappush(h, q.popleft()[0])
        return time
