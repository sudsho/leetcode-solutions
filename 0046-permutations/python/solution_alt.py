# itertools cheat (would not use in interview)
from itertools import permutations
class Solution:
    def permute(self, nums):
        return [list(p) for p in permutations(nums)]
