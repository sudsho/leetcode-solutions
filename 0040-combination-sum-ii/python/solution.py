class Solution:
    def combinationSum2(self, candidates, target):
        candidates.sort()
        out = []
        path = []

        def go(start, remaining):
            if remaining == 0:
                out.append(path[:])
                return
            for i in range(start, len(candidates)):
                if candidates[i] > remaining:
                    break
                # skip duplicates at the same recursion level
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                path.append(candidates[i])
                go(i + 1, remaining - candidates[i])
                path.pop()

        go(0, target)
        return out
