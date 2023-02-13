# 2023 nit (18)
# segment tree on value rank
from typing import List

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        sorted_unique = sorted(set(nums))
        rank = {v: i for i, v in enumerate(sorted_unique)}
        tree = [0] * (len(sorted_unique) + 1)

        def update(i: int) -> None:
            i += 1
            while i < len(tree):
                tree[i] += 1
                i += i & -i

        def query(i: int) -> int:
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & -i
            return s

        result = [0] * len(nums)
        for k in range(len(nums) - 1, -1, -1):
            r = rank[nums[k]]
            result[k] = query(r)
            update(r)
        return result
