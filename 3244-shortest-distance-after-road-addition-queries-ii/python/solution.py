from typing import List
from sortedcontainers import SortedList

class Solution:
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        # represent active "next" pointers using a sorted list of nodes still in the chain
        sl = SortedList(range(n))
        ans: list[int] = []
        for u, v in queries:
            i = sl.bisect_right(u)
            # remove nodes strictly between u and v
            while i < len(sl) and sl[i] < v:
                sl.pop(i)
            ans.append(len(sl) - 1)
        return ans
# revisit
