class Solution:
    def combinationSum3(self, k, n):
        """Find all combinations of k distinct digits 1..9 summing to n.

        Backtrack over digits in increasing order so each combination is built
        once. Prune early: if the running sum already exceeds n, or even the
        smallest remaining digits cannot reach n, abandon the branch.
        """
        result = []
        combo = []

        def backtrack(start, remaining):
            if len(combo) == k:
                if remaining == 0:
                    result.append(combo[:])
                return
            for d in range(start, 10):
                # digits only grow from here, so once d alone overshoots the
                # remaining target the rest of the branch is hopeless.
                if d > remaining:
                    break
                combo.append(d)
                backtrack(d + 1, remaining - d)
                combo.pop()

        backtrack(1, n)
        return result
