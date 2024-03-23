from typing import List

class Solution:
    def shortestSuperstring(self, words: List[str]) -> str:
        n = len(words)
        overlap = [[0] * n for _ in range(n)]
        for i, a in enumerate(words):
            for j, b in enumerate(words):
                if i == j:
                    continue
                lim = min(len(a), len(b))
                for k in range(lim, 0, -1):
                    if a[-k:] == b[:k]:
                        overlap[i][j] = k
                        break
        INF = -10 ** 9
        dp = [[INF] * n for _ in range(1 << n)]
        parent = [[-1] * n for _ in range(1 << n)]
        for i in range(n):
            dp[1 << i][i] = len(words[i])
        for mask in range(1 << n):
            for i in range(n):
                if not mask & (1 << i):
                    continue
                for j in range(n):
                    if mask & (1 << j):
                        continue
                    cand = dp[mask][i] + len(words[j]) - overlap[i][j]
                    nm = mask | (1 << j)
                    if cand > dp[nm][j]:
                        dp[nm][j] = cand
                        parent[nm][j] = i
        full = (1 << n) - 1
        end = max(range(n), key=lambda i: dp[full][i])
        path: list[int] = []
        cur, mask = end, full
        while cur != -1:
            path.append(cur)
            p = parent[mask][cur]
            mask ^= 1 << cur
            cur = p
        path.reverse()
        result = words[path[0]]
        for k in range(1, len(path)):
            result += words[path[k]][overlap[path[k - 1]][path[k]]:]
        return result
# style tweak
