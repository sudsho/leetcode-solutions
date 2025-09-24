from typing import List
from collections import defaultdict

class Solution:
    def countServers(self, n: int, logs: List[List[int]], x: int, queries: List[int]) -> List[int]:
        logs.sort(key=lambda r: r[1])
        order = sorted(range(len(queries)), key=lambda i: queries[i])
        ans = [0] * len(queries)
        cnt: dict[int, int] = defaultdict(int)
        l = r = 0
        for i in order:
            t = queries[i]
            while r < len(logs) and logs[r][1] <= t:
                cnt[logs[r][0]] += 1
                r += 1
            while l < len(logs) and logs[l][1] < t - x:
                cnt[logs[l][0]] -= 1
                if cnt[logs[l][0]] == 0:
                    del cnt[logs[l][0]]
                l += 1
            ans[i] = n - len(cnt)
        return ans
