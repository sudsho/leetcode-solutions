class Solution:
    def combinationSum(self, candidates, target):
        candidates.sort()
        out = []
        def go(start, remain, path):
            if remain == 0:
                out.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:
                    break
                path.append(candidates[i])
                go(i, remain - candidates[i], path)
                path.pop()
        go(0, target, [])
        return out
