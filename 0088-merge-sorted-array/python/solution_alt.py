# alt approach: lazy: copy + sort. O((n+m) log(n+m)) but trivial to write

class Solution:
    def merge(self, nums1, m, nums2, n):
        # easy way - copy and sort. not O(1) extra space
        nums1[m:] = nums2[:n]
        nums1.sort()
