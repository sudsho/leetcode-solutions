from typing import List

class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        prefix = [0]
        for n in nums:
            prefix.append(prefix[-1] + n)

        def sort_count(lo: int, hi: int) -> int:
            if hi - lo <= 1:
                return 0
            mid = (lo + hi) // 2
            count = sort_count(lo, mid) + sort_count(mid, hi)
            i = j = mid
            for left in prefix[lo:mid]:
                while i < hi and prefix[i] - left < lower:
                    i += 1
                while j < hi and prefix[j] - left <= upper:
                    j += 1
                count += j - i
            prefix[lo:hi] = sorted(prefix[lo:hi])
            return count

        return sort_count(0, len(prefix))
