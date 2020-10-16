class Solution:
    def permute(self, nums):
        out = []
        def go(path, used):
            if len(path) == len(nums):
                out.append(path[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                go(path, used)
                path.pop()
                used[i] = False
        go([], [False] * len(nums))
        return out
