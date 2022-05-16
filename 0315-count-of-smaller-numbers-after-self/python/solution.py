from typing import List

class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        idx = list(range(n))

        def merge_sort(lo: int, hi: int) -> List[int]:
            if hi - lo <= 1:
                return idx[lo:hi]
            mid = (lo + hi) // 2
            left = merge_sort(lo, mid)
            right = merge_sort(mid, hi)
            merged: List[int] = []
            i = j = 0
            right_count = 0
            while i < len(left) and j < len(right):
                if nums[left[i]] <= nums[right[j]]:
                    result[left[i]] += right_count
                    merged.append(left[i])
                    i += 1
                else:
                    right_count += 1
                    merged.append(right[j])
                    j += 1
            while i < len(left):
                result[left[i]] += right_count
                merged.append(left[i])
                i += 1
            merged.extend(right[j:])
            for k, v in enumerate(merged):
                idx[lo + k] = v
            return merged

        merge_sort(0, n)
        return result
