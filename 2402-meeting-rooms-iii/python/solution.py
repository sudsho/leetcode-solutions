from heapq import heappush, heappop
from typing import List

class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        free: list[int] = list(range(n))
        busy: list[tuple[int, int]] = []
        count = [0] * n
        for start, end in meetings:
            while busy and busy[0][0] <= start:
                _, room = heappop(busy)
                heappush(free, room)
            if free:
                room = heappop(free)
                heappush(busy, (end, room))
            else:
                t, room = heappop(busy)
                heappush(busy, (t + (end - start), room))
            count[room] += 1
        best = 0
        for i in range(1, n):
            if count[i] > count[best]:
                best = i
        return best
# small fix
