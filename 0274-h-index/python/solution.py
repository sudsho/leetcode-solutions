class Solution:
    def hIndex(self, citations):
        # counting-sort variant: h can never exceed the number of papers, so
        # bucket every citation count, clamping anything above n into bucket n
        n = len(citations)
        buckets = [0] * (n + 1)
        for c in citations:
            buckets[min(c, n)] += 1
        # sweep h from high to low, accumulating how many papers have >= h
        # citations; the first h where that running total reaches h is the answer
        total = 0
        for h in range(n, -1, -1):
            total += buckets[h]
            if total >= h:
                return h
        return 0
