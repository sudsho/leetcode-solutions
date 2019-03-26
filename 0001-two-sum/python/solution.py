class Solution:
    def twoSum(self, nums, target):
        # walk once, store value -> index in a dict
        seen = {}
        for i, n in enumerate(nums):
            need = target - n
            if need in seen:
                return [seen[need], i]
            seen[n] = i
        # problem says one solution always exists so we should not get here
        return []
