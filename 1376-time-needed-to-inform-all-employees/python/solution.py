from typing import List
from collections import defaultdict

class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        children = defaultdict(list)
        for i, m in enumerate(manager):
            if m != -1:
                children[m].append(i)

        def dfs(u: int) -> int:
            if not children[u]:
                return 0
            return informTime[u] + max(dfs(c) for c in children[u])

        return dfs(headID)
