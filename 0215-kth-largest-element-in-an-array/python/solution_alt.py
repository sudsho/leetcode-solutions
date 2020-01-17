import random

class Solution:
    def findKthLargest(self, nums, k):
        # quickselect - O(n) average
        target = len(nums) - k

        def select(l, r):
            pivot = nums[random.randint(l, r)]
            lo, mid, hi = l, l, r
            while mid <= hi:
                if nums[mid] < pivot:
                    nums[lo], nums[mid] = nums[mid], nums[lo]
                    lo += 1
                    mid += 1
                elif nums[mid] > pivot:
                    nums[mid], nums[hi] = nums[hi], nums[mid]
                    hi -= 1
                else:
                    mid += 1
            if target < lo:
                return select(l, lo - 1)
            if target > hi:
                return select(hi + 1, r)
            return nums[target]

        return select(0, len(nums) - 1)
