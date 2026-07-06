# alt: sort descending, the h-index is the last position where citations[i] > i
class Solution:
    def hIndex(self, citations):
        citations.sort(reverse=True)
        h = 0
        for i, c in enumerate(citations):
            # paper at 0-based rank i is the (i+1)-th most cited; it can only
            # count toward an h-index of i+1 if it has at least i+1 citations
            if c >= i + 1:
                h = i + 1
            else:
                break
        return h
