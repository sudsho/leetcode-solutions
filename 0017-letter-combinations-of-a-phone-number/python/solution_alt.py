# iterative version using a running list
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        m = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
             "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
        result = [""]
        for d in digits:
            result = [prev + ch for prev in result for ch in m[d]]
        return result
