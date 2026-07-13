from typing import List
import bisect

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        """Fenwick / BIT variant with coordinate compression.

        Walk left to right and, before inserting nums[i], ask how many values
        already seen are strictly greater than 2 * nums[i] -- those are exactly
        the earlier indices that form a reverse pair with i. To make that a
        prefix query, compress both the raw values and the doubled thresholds
        into one sorted coordinate space, then query the suffix as (total so
        far) - (count <= 2 * nums[i]).
        """
        # Coordinate space: every value we might rank or threshold against.
        coords = sorted(set(nums) | {2 * v for v in nums})
        rank = {v: i + 1 for i, v in enumerate(coords)}  # 1-indexed for BIT
        size = len(coords)

        tree = [0] * (size + 1)

        def update(i: int) -> None:
            while i <= size:
                tree[i] += 1
                i += i & (-i)

        def query(i: int) -> int:
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        count = 0
        seen = 0
        for v in nums:
            # Rank of the largest coord <= 2*v; anything above it is > 2*v.
            pos = bisect.bisect_right(coords, 2 * v)
            count += seen - query(pos)
            update(rank[v])
            seen += 1
        return count
