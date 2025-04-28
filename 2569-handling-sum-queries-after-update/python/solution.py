from typing import List

class Solution:
    def handleQuery(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums1)
        # segment tree storing count of 1s in range, lazy flip
        size = 1
        while size < n:
            size <<= 1
        cnt = [0] * (2 * size)
        lazy = [0] * (2 * size)
        for i, v in enumerate(nums1):
            cnt[size + i] = v
        for i in range(size - 1, 0, -1):
            cnt[i] = cnt[2 * i] + cnt[2 * i + 1]
        seg_size = [1] * (2 * size)
        for i in range(size - 1, 0, -1):
            seg_size[i] = seg_size[2 * i] + seg_size[2 * i + 1]

        def apply(i: int) -> None:
            cnt[i] = seg_size[i] - cnt[i]
            lazy[i] ^= 1

        def push(i: int) -> None:
            if lazy[i]:
                apply(2 * i)
                apply(2 * i + 1)
                lazy[i] = 0

        def upd(i: int, l: int, r: int, ql: int, qr: int) -> None:
            if qr <= l or r <= ql:
                return
            if ql <= l and r <= qr:
                apply(i)
                return
            push(i)
            m = (l + r) // 2
            upd(2 * i, l, m, ql, qr)
            upd(2 * i + 1, m, r, ql, qr)
            cnt[i] = cnt[2 * i] + cnt[2 * i + 1]

        s2 = sum(nums2)
        ans: list[int] = []
        for q in queries:
            if q[0] == 1:
                upd(1, 0, size, q[1], q[2] + 1)
            elif q[0] == 2:
                s2 += q[1] * cnt[1]
            else:
                ans.append(s2)
        return ans
