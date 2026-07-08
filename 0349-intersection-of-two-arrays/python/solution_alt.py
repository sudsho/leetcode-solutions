# alt: two-pointer version if the inputs were already sorted (or worth sorting).
# avoids building two sets - handy when memory matters more than the sort cost.

class Solution:
    def intersection(self, nums1, nums2):
        nums1.sort()
        nums2.sort()
        i, j = 0, 0
        out = []
        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                i += 1
            elif nums1[i] > nums2[j]:
                j += 1
            else:
                # equal - record it, then skip every duplicate of this value on
                # both sides so it only lands in the answer once
                if not out or out[-1] != nums1[i]:
                    out.append(nums1[i])
                i += 1
                j += 1
        return out
