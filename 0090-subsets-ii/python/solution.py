# subsets ii - the array can contain duplicates, so we have to avoid
# emitting the same subset twice. sort first, then when we're choosing
# whether to include nums[i] at a given depth, skip any duplicate value
# that we've already had a chance to pick at this same level.

class Solution:
    def subsetsWithDup(self, nums):
        nums.sort()
        res = []
        path = []

        def backtrack(start):
            res.append(path[:])
            for i in range(start, len(nums)):
                # i > start means this value is a sibling choice at this level,
                # not the first time we see it on this branch - skip the dup
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return res
