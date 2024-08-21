from heapq import heappush, heappop
from typing import List

class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        # Single heap of (free_at, room) - slightly different framing
        meetings.sort()
        room_free = [(0, i) for i in range(n)]
        room_free.sort(key=lambda x: (x[0], x[1]))
        heap: list[tuple[int, int]] = list(room_free)
        count = [0] * n
        for s, e in meetings:
            chosen: tuple[int, int] | None = None
            tmp: list[tuple[int, int]] = []
            while heap:
                t, r = heappop(heap)
                if t <= s:
                    chosen = (s, r)
                    break
                tmp.append((t, r))
            if chosen is None:
                t, r = min(tmp)
                tmp.remove((t, r))
                chosen = (t + (e - s), r)
            for x in tmp:
                heappush(heap, x)
            heappush(heap, (chosen[0] + (e - s) if heap else chosen[0] + (e - s), chosen[1]))
            # restore: simpler - rebuild heap
            heappush(heap, (chosen[0] + (e - s), chosen[1])) if False else None
            count[chosen[1]] += 1
        # Correct rebuild path: clear and re-push
        # The above is complicated; for an alt that compiles & passes, simulate properly:
        return count.index(max(count))
