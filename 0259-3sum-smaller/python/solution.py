class Solution:
    def threeSumSmaller(self, nums, target):
        # sort so we can sweep two pointers per fixed first element.
        nums.sort()
        n = len(nums)
        count = 0
        for i in range(n - 2):
            lo, hi = i + 1, n - 1
            while lo < hi:
                if nums[i] + nums[lo] + nums[hi] < target:
                    # nums is sorted, so every hi' in (lo, hi] also keeps
                    # the sum under target -> that's (hi - lo) triplets at once,
                    # then advance lo to look for more with a larger middle.
                    count += hi - lo
                    lo += 1
                else:
                    # sum too big, only shrinking the largest term can help.
                    hi -= 1
        return count
