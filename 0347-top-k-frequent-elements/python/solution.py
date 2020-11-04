from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        cnt = Counter(nums)
        # bucket sort by frequency
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, c in cnt.items():
            buckets[c].append(num)
        out = []
        for c in range(len(buckets) - 1, 0, -1):
            for num in buckets[c]:
                out.append(num)
                if len(out) == k:
                    return out
        return out
