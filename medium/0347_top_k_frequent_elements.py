"""
LeetCode 347 - Top K Frequent Elements.
Given an integer array nums and an integer k, return the k most frequent
elements. Bucket-sort solution runs in linear time on the count distribution.
"""

from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)

        # buckets[i] holds all numbers with frequency i. Max possible
        # frequency is len(nums), so we need len(nums) + 1 buckets.
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in counts.items():
            buckets[freq].append(num)

        result = []
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                result.append(num)
                if len(result) == k:
                    return result
        return result

    def topKFrequentHeap(self, nums: List[int], k: int) -> List[int]:
        import heapq
        counts = Counter(nums)
        return [num for num, _ in heapq.nlargest(k, counts.items(), key=lambda x: x[1])]


# Time: O(n) for the bucket-sort version, O(n log k) for the heap version.
# Space: O(n) for the counter and buckets.

if __name__ == "__main__":
    sol = Solution()
    print(sorted(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)))  # [1, 2]
    print(sorted(sol.topKFrequent([1], 1)))  # [1]
    print(sorted(sol.topKFrequent([4, 4, 4, 5, 5, 6], 2)))  # [4, 5]
