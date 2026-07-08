from collections import Counter


class Solution:
    def intersect(self, nums1, nums2):
        # unlike 349, this one keeps multiplicity: a value that appears twice in
        # both arrays should show up twice. count one side, then walk the other
        # spending from those counts.
        counts = Counter(nums1)
        out = []
        for n in nums2:
            if counts[n] > 0:
                out.append(n)
                counts[n] -= 1
        return out
