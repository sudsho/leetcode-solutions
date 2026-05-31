class Solution:
    def reverseString(self, s):
        """Reverse the character list in place with two pointers from both ends."""
        i, j = 0, len(s) - 1
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
