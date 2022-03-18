from typing import List

class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        order = sorted(range(len(queries)), key=lambda i: queries[i][1])
        result = [-1] * len(queries)
        BITS = 30
        root: dict = {}

        def insert(x: int) -> None:
            node = root
            for b in range(BITS, -1, -1):
                bit = (x >> b) & 1
                node = node.setdefault(bit, {})

        def query(x: int) -> int:
            if not root:
                return -1
            node = root
            ans = 0
            for b in range(BITS, -1, -1):
                bit = (x >> b) & 1
                want = 1 - bit
                if want in node:
                    ans |= (1 << b)
                    node = node[want]
                else:
                    node = node[bit]
            return ans

        i = 0
        for q in order:
            x, m = queries[q]
            while i < len(nums) and nums[i] <= m:
                insert(nums[i])
                i += 1
            result[q] = query(x)
        return result
