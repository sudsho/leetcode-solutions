class Solution:
    def subsets(self, nums):
        out = []
        def go(i, path):
            if i == len(nums):
                out.append(path[:])
                return
            # skip
            go(i + 1, path)
            # include
            path.append(nums[i])
            go(i + 1, path)
            path.pop()
        go(0, [])
        return out
# notes: tightened naming
# typing fix
