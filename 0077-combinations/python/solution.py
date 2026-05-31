class Solution:
    def combine(self, n, k):
        out = []
        path = []

        def backtrack(start):
            if len(path) == k:
                out.append(path[:])
                return
            # prune: need k - len(path) more elements; last usable start
            # is n - (k - len(path)) + 1 inclusive
            need = k - len(path)
            for i in range(start, n - need + 2):
                path.append(i)
                backtrack(i + 1)
                path.pop()

        backtrack(1)
        return out
