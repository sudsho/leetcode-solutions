from typing import List
from sortedcontainers import SortedList

class Solution:
    def getResults(self, queries: List[List[int]]) -> List[bool]:
        obstacles = SortedList([0])
        # segment tree on positions 1..N tracking max gap up to that position
        N = 50_001
        tree = [0] * (4 * N)
        gaps = [0] * (N + 2)

        def update(idx: int, val: int, i: int = 1, l: int = 1, r: int = N) -> None:
            if l == r:
                tree[i] = val
                return
            m = (l + r) // 2
            if idx <= m:
                update(idx, val, 2 * i, l, m)
            else:
                update(idx, val, 2 * i + 1, m + 1, r)
            tree[i] = max(tree[2 * i], tree[2 * i + 1])

        def query_le(x: int, i: int = 1, l: int = 1, r: int = N) -> int:
            if r <= x:
                return tree[i]
            if l > x:
                return 0
            m = (l + r) // 2
            return max(query_le(x, 2 * i, l, m), query_le(x, 2 * i + 1, m + 1, r))

        ans: list[bool] = []
        for q in queries:
            if q[0] == 1:
                x = q[1]
                idx = obstacles.bisect_left(x)
                left_obs = obstacles[idx - 1]
                if idx < len(obstacles):
                    right_obs = obstacles[idx]
                    # update gaps for the cut
                    new_left_gap = x - left_obs
                    update(x, new_left_gap)
                    new_right_gap = right_obs - x
                    update(right_obs, new_right_gap)
                else:
                    new_left_gap = x - left_obs
                    update(x, new_left_gap)
                obstacles.add(x)
            else:
                x, sz = q[1], q[2]
                # find largest gap with right-endpoint <= x
                idx = obstacles.bisect_right(x) - 1
                # the obstacle <= x exists since 0 is included
                # max gap among segments fully before x:
                # plus the current open segment (last_obs..x)
                last = obstacles[idx]
                gap_at_x = x - last
                max_left = query_le(last) if last >= 1 else 0
                ans.append(max(max_left, gap_at_x) >= sz)
        return ans
