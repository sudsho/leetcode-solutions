from typing import List

class TreeAncestor:
    def __init__(self, n: int, parent: List[int]):
        LOG = 1
        while (1 << LOG) < n:
            LOG += 1
        self.LOG = LOG
        self.up = [parent[:]]
        for i in range(1, LOG):
            prev = self.up[-1]
            cur = [-1] * n
            for v in range(n):
                if prev[v] != -1:
                    cur[v] = prev[prev[v]]
            self.up.append(cur)

    def getKthAncestor(self, node: int, k: int) -> int:
        for i in range(self.LOG):
            if k >> i & 1:
                node = self.up[i][node]
                if node == -1:
                    return -1
        return node
