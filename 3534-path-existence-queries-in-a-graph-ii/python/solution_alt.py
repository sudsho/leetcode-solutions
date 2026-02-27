# alt: layered BFS per query (works for small graphs only, verifies the sparse table)
from typing import List


class Solution:
    def pathExistenceQueries(self, n: int, nums: List[int], maxDiff: int, queries: List[List[int]]) -> List[int]:
        # build sorted order
        idx_sorted = sorted(range(n), key=lambda i: nums[i])
        order = [0] * n
        for k, i in enumerate(idx_sorted):
            order[i] = k
        # adjacency: in sorted order, edges between i and i+1 if diff small
        ans = []
        for u, v in queries:
            if u == v:
                ans.append(0)
                continue
            ou, ov = order[u], order[v]
            if ou > ov:
                ou, ov = ov, ou
            steps = 0
            cur = ou
            while cur < ov:
                # greedy: jump as far as possible
                far = cur
                while far + 1 < n and nums[idx_sorted[far + 1]] - nums[idx_sorted[cur]] <= maxDiff:
                    far += 1
                if far == cur:
                    ans.append(-1)
                    break
                cur = far
                steps += 1
            else:
                ans.append(steps)
        return ans
