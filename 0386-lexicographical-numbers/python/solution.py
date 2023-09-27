from typing import List

class Solution:
    def lexicalOrder(self, n: int) -> List[int]:
        out: list[int] = []
        cur = 1
        for _ in range(n):
            out.append(cur)
            if cur * 10 <= n:
                cur *= 10
            else:
                while cur % 10 == 9 or cur + 1 > n:
                    cur //= 10
                cur += 1
        return out
