from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n

        def rev(i: int, j: int) -> None:
            while i < j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1; j -= 1

        rev(0, n - 1)
        rev(0, k - 1)
        rev(k, n - 1)

# revisit: minor renames and one early exit added
