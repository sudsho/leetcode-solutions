# alt approach: one-liner using str.find (cheating but valid)

class Solution:
    def strStr(self, haystack, needle):
        # python find does it in one line. trivia answer
        return haystack.find(needle)
