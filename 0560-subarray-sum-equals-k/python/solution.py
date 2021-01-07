from collections import defaultdict

class Solution:
    def subarraySum(self, nums, k):
        seen = defaultdict(int)
        seen[0] = 1
        cur = 0
        count = 0
        for x in nums:
            cur += x
            count += seen[cur - k]
            seen[cur] += 1
        return count
# notes: tightened naming
