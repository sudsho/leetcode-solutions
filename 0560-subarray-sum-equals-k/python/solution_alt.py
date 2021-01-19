# alt with explicit prefix counter and tighter loop
from collections import defaultdict
from typing import List

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        seen = defaultdict(int)
        seen[0] = 1
        cur = ans = 0
        for x in nums:
            cur += x
            ans += seen[cur - k]
            seen[cur] += 1
        return ans
