# linear scan handles duplicates trivially
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        return target in nums
