class Solution:
    def tilingRectangle(self, n: int, m: int) -> int:
        if n > m:
            n, m = m, n
        best = [n * m]
        skyline = [0] * m
        def dfs(used: int) -> None:
            if used >= best[0]:
                return
            mn = min(skyline)
            if mn == n:
                best[0] = used
                return
            i = skyline.index(mn)
            j = i
            while j < m and skyline[j] == mn and j - i + 1 + mn <= n:
                j += 1
            sz = j - i
            for s in range(sz, 0, -1):
                if mn + s > n:
                    continue
                for k in range(i, i + s):
                    skyline[k] += s
                dfs(used + 1)
                for k in range(i, i + s):
                    skyline[k] -= s
        dfs(0)
        return best[0]
