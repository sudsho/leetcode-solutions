from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        """Summarize a sorted, distinct int array as its consecutive ranges.

        Each maximal run of consecutive integers becomes one entry: a lone value
        renders as "a" and a run of two or more as "a->b". One linear pass over
        the array is enough since it is already sorted with no duplicates.
        """
        # Walk the sorted array once, extending the current run while each value
        # is exactly one more than the previous. When the run breaks, emit it as
        # either "a" (single value) or "a->b" (range), then start a fresh run.
        ranges: List[str] = []
        n = len(nums)
        i = 0
        while i < n:
            start = nums[i]
            # advance j over the contiguous run start, start+1, start+2, ...
            while i + 1 < n and nums[i + 1] == nums[i] + 1:
                i += 1
            end = nums[i]
            ranges.append(str(start) if start == end else f"{start}->{end}")
            i += 1
        return ranges
