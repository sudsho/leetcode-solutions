from typing import List

class Solution:
    def matrixSumQueries(self, n: int, queries: List[List[int]]) -> int:
        rows_free, cols_free = n, n
        seen_row, seen_col = set(), set()
        ans = 0
        for t, idx, val in reversed(queries):
            if t == 0:
                if idx in seen_row:
                    continue
                seen_row.add(idx)
                ans += val * cols_free
                rows_free -= 1
            else:
                if idx in seen_col:
                    continue
                seen_col.add(idx)
                ans += val * rows_free
                cols_free -= 1
        return ans
