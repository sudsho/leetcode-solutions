from typing import List

class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[int]:
        # nums sorted? we treat positions as nodes; edge i->i+1 if diff small
        idx_sorted = sorted(range(n), key=lambda i: nums[i])
        order = [0] * n
        for k, i in enumerate(idx_sorted):
            order[i] = k
        # in sorted order, build next jump arr
        nxt = [0] * n
        j = 0
        for i in range(n):
            if j < i:
                j = i
            while j + 1 < n and nums[idx_sorted[j + 1]] - nums[idx_sorted[i]] <= maxDiff:
                j += 1
            nxt[i] = j
        LOG = 17
        jmp = [nxt[:]] + [[0] * n for _ in range(LOG - 1)]
        for k in range(1, LOG):
            for i in range(n):
                jmp[k][i] = jmp[k - 1][jmp[k - 1][i]]
        ans: list[int] = []
        for u, v in queries:
            ou, ov = order[u], order[v]
            if ou > ov:
                ou, ov = ov, ou
            if abs(nums[u] - nums[v]) <= maxDiff:
                ans.append(1 if u != v else 0)
                continue
            steps = 0
            cur = ou
            for k in range(LOG - 1, -1, -1):
                if jmp[k][cur] < ov:
                    cur = jmp[k][cur]
                    steps += (1 << k)
            if jmp[0][cur] >= ov:
                steps += 1
                ans.append(steps)
            else:
                ans.append(-1)
        return ans
