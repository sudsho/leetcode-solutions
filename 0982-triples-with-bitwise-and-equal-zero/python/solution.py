from collections import Counter
from typing import List

class Solution:
    def countTriplets(self, nums: List[int]) -> int:
        pair = Counter()
        for a in nums:
            for b in nums:
                pair[a & b] += 1
        ans = 0
        for c in nums:
            for k, v in pair.items():
                if c & k == 0:
                    ans += v
        return ans
