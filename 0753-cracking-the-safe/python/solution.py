class Solution:
    def crackSafe(self, n: int, k: int) -> str:
        seen: set[str] = set()
        out: list[str] = []
        start = '0' * (n - 1)
        def dfs(node: str) -> None:
            for d in map(str, range(k)):
                e = node + d
                if e not in seen:
                    seen.add(e)
                    dfs(e[1:])
                    out.append(d)
        dfs(start)
        return ''.join(out) + start
