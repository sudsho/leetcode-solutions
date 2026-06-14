class Solution:
    def reverseWords(self, s):
        """Reverse the order of words in s, collapsing runs of spaces.

        split() with no argument already does the heavy lifting: it splits on
        arbitrary whitespace and drops leading, trailing, and repeated spaces.
        Reverse the resulting word list and join with a single space.
        """
        return " ".join(reversed(s.split()))
