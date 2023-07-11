# 2023 nit (126)
# offline alt: bit walk with per-bit prefix counts
from typing import List

class Solution:
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        Q = len(queries)
        order = sorted(range(Q), key=lambda i: queries[i][1])
        result = [-1] * Q
        BITS = 30

        # Build incremental trie
        root: dict = {}
        i = 0
        for q in order:
            x, m = queries[q]
            while i < len(nums) and nums[i] <= m:
                node = root
                for b in range(BITS, -1, -1):
                    bit = (nums[i] >> b) & 1
                    node = node.setdefault(bit, {})
                i += 1
            if not root:
                continue
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
            result[q] = ans
        return result
