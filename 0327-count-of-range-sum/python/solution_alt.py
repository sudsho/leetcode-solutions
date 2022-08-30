# BIT version: keep sorted prefix sums and do range queries
from typing import List
from bisect import bisect_left, bisect_right, insort

class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        prefix = 0
        seen = [0]
        count = 0
        for n in nums:
            prefix += n
            lo = bisect_left(seen, prefix - upper)
            hi = bisect_right(seen, prefix - lower)
            count += hi - lo
            insort(seen, prefix)
        return count
