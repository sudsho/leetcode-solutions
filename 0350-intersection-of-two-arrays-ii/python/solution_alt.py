# alt: sort both and two-pointer. this is the version the follow-up asks about
# for when the arrays are already sorted or too big to hold a counter for.

class Solution:
    def intersect(self, nums1, nums2):
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
                # equal on both sides - take one copy and advance both, which
                # naturally preserves the min multiplicity across the two arrays
                out.append(nums1[i])
                i += 1
                j += 1
        return out
