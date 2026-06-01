class Solution:
    def permuteUnique(self, nums):
        nums.sort()
        out = []
        used = [False] * len(nums)

        def go(path):
            if len(path) == len(nums):
                out.append(path[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                    continue
                used[i] = True
                path.append(nums[i])
                go(path)
                path.pop()
                used[i] = False

        go([])
        return out
