from collections import Counter


class Solution:
    def fourSumCount(self, nums1, nums2, nums3, nums4):
        """Count tuples (i, j, k, l) with nums1[i]+nums2[j]+nums3[k]+nums4[l] == 0.

        The brute force over all four arrays is O(n^4). Split the four arrays
        into two halves instead: tally every pairwise sum from the first two
        arrays in a Counter, then for each pairwise sum from the last two look
        up how many first-half sums cancel it. Each half is O(n^2), so the whole
        thing is O(n^2) time and O(n^2) space for the Counter.
        """
        first_half = Counter(a + b for a in nums1 for b in nums2)
        count = 0
        for c in nums3:
            for d in nums4:
                # we need a + b == -(c + d) for the total to be zero
                count += first_half[-(c + d)]
        return count
