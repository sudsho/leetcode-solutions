class Solution:
    def findMaxLength(self, nums):
        # map 0 -> -1 so a balanced stretch sums to exactly zero, which turns
        # "equal counts of 0 and 1" into "two prefix sums are the same".
        # first_seen[s] = earliest index where running sum s appeared.
        # sum 0 is "seen" at index -1 so a prefix that balances on its own counts.
        first_seen = {0: -1}
        running = 0
        best = 0
        for i, v in enumerate(nums):
            running += 1 if v == 1 else -1
            if running in first_seen:
                # same sum twice means the slice between them nets to zero
                best = max(best, i - first_seen[running])
            else:
                # only record the FIRST index - keeping the earliest one is what
                # makes every later match give the longest possible window.
                first_seen[running] = i
        return best
