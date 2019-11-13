# alt approach: hash set version. uses extra space but easier to reason about

class Solution:
    def singleNumber(self, nums):
        # hash set version - O(n) extra space but easier to think about
        seen = set()
        for n in nums:
            if n in seen:
                seen.remove(n)
            else:
                seen.add(n)
        # whatever is left is the answer
        return seen.pop()
