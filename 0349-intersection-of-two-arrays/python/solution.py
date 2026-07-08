class Solution:
    def intersection(self, nums1, nums2):
        # the result is a *set* intersection - each common value appears once,
        # order does not matter. two hash sets and the & operator do it directly.
        a, b = set(nums1), set(nums2)
        return list(a & b)
