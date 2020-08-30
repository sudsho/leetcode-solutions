# iterative: build power set by extending each existing subset
class Solution:
    def subsets(self, nums):
        result = [[]]
        for n in nums:
            result += [r + [n] for r in result]
        return result
