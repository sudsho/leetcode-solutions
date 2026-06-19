class Solution:
    def increasingTriplet(self, nums):
        """Return True if some i < j < k has nums[i] < nums[j] < nums[k].
        Keep the smallest value seen (first) and the smallest value that already
        has something smaller before it (second). A value beating second closes
        a length-3 increasing chain. O(1) memory, no actual indices stored."""
        first = float("inf")
        second = float("inf")
        for n in nums:
            if n <= first:
                first = n          # new smallest candidate for i
            elif n <= second:
                second = n         # n has a smaller element before it -> valid j
            else:
                return True        # n is greater than some valid second -> triplet
        return False
