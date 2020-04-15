# bisect helper
from bisect import bisect_left
class Solution:
    def searchInsert(self, nums, target):
        return bisect_left(nums, target)
