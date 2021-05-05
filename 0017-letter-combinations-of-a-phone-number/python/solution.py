# style tweak
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        m = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
             "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        out = []
        def backtrack(i, path):
            if i == len(digits):
                out.append("".join(path))
                return
            for ch in m[digits[i]]:
                path.append(ch)
                backtrack(i + 1, path)
                path.pop()
        backtrack(0, [])
        return out
# notes: tightened naming
