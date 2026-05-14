class Solution:
    def maximumGap(self, nums):
        n = len(nums)
        if n < 2:
            return 0

        lo, hi = min(nums), max(nums)
        if lo == hi:
            return 0

        # bucket sort idea. with n numbers in [lo, hi] the maximum gap is at
        # least ceil((hi - lo) / (n - 1)). pick that as bucket width and only
        # one bucket can be empty in the optimum case, so the answer is
        # always between adjacent non-empty buckets - never within a bucket.
        width = max(1, (hi - lo) // (n - 1))
        bucket_count = (hi - lo) // width + 1
        buckets = [None] * bucket_count

        for x in nums:
            idx = (x - lo) // width
            b = buckets[idx]
            if b is None:
                buckets[idx] = [x, x]
            else:
                if x < b[0]:
                    b[0] = x
                if x > b[1]:
                    b[1] = x

        best = 0
        prev_high = None
        for b in buckets:
            if b is None:
                continue
            if prev_high is not None:
                best = max(best, b[0] - prev_high)
            prev_high = b[1]
        return best
