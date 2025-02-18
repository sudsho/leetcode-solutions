from typing import List

class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int) -> int:
        # transform: count pairs i<j where d[i] <= d[j] + diff, where d=nums1-nums2
        d = [a - b for a, b in zip(nums1, nums2)]

        def merge_count(arr: list[int], l: int, r: int) -> int:
            if r - l <= 1:
                return 0
            m = (l + r) // 2
            cnt = merge_count(arr, l, m) + merge_count(arr, m, r)
            j = m
            for i in range(l, m):
                while j < r and arr[j] + diff < arr[i]:
                    j += 1
                cnt += r - j
            arr[l:r] = sorted(arr[l:r])
            return cnt

        return merge_count(d, 0, len(d))
