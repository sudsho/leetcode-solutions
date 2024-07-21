from typing import List

class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        # flatten + sliding window over k buckets
        merged: list[tuple[int, int]] = []
        for i, row in enumerate(nums):
            for v in row:
                merged.append((v, i))
        merged.sort()
        k = len(nums)
        cnt = [0] * k
        have = 0
        left = 0
        best = [merged[0][0], merged[-1][0]]
        for right in range(len(merged)):
            v, idx = merged[right]
            if cnt[idx] == 0:
                have += 1
            cnt[idx] += 1
            while have == k:
                lv, li = merged[left]
                if v - lv < best[1] - best[0]:
                    best = [lv, v]
                cnt[li] -= 1
                if cnt[li] == 0:
                    have -= 1
                left += 1
        return best
