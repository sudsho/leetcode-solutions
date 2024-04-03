from typing import List
from sortedcontainers import SortedList

class Solution:
    def oddEvenJumps(self, arr: List[int]) -> int:
        # SortedList for next-greater-equal / next-smaller-equal
        n = len(arr)
        odd = [False] * n
        even = [False] * n
        odd[-1] = even[-1] = True
        sl: SortedList = SortedList([(arr[-1], n - 1)])
        ans = 1
        for i in range(n - 2, -1, -1):
            v = arr[i]
            idx_ge = sl.bisect_left((v, -1))
            if idx_ge < len(sl):
                _, j = sl[idx_ge]
                if even[j]:
                    odd[i] = True
                    ans += 1
            idx_le = sl.bisect_right((v, n))
            if idx_le > 0:
                _, j = sl[idx_le - 1]
                if odd[j]:
                    even[i] = True
            sl.add((v, i))
        return ans
