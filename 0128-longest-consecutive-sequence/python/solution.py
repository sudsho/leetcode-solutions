class Solution:
    def longestConsecutive(self, nums):
        s = set(nums)
        best = 0
        for n in s:
            if n - 1 not in s:
                cur = n
                length = 1
                while cur + 1 in s:
                    cur += 1
                    length += 1
                if length > best:
                    best = length
        return best
