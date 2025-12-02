from typing import List

class Solution:
    def minDifference(self, nums: List[int]) -> int:
        n = len(nums)
        # collect anchors and the max forced difference among pairs without -1
        forced = 0
        anchors_low = []
        anchors_high = []
        i = 0
        while i < n:
            if nums[i] != -1:
                if i + 1 < n and nums[i + 1] != -1:
                    forced = max(forced, abs(nums[i] - nums[i + 1]))
                i += 1
                continue
            j = i
            while j < n and nums[j] == -1:
                j += 1
            left = nums[i - 1] if i > 0 else None
            right = nums[j] if j < n else None
            if left is not None and right is not None:
                anchors_low.append(min(left, right))
                anchors_high.append(max(left, right))
            elif left is not None:
                anchors_low.append(left)
                anchors_high.append(left)
            elif right is not None:
                anchors_low.append(right)
                anchors_high.append(right)
            # else all -1; trivially 0
            i = j

        def feasible(d: int) -> bool:
            # choose x and y; check there exist x,y in [1..1e9] s.t. for every anchor pair (lo, hi):
            # min(|x - lo|, |x - hi|, |y - lo|, |y - hi|, |x-y| / 2 ...) <= d, plus segment-internal differences absorbed by |x-y|<=d
            # Simplified test: for each (lo, hi), at least one of {x, y} should be within d of lo and another within d of hi
            # We try assigning a candidate: take each anchor's needed range and intersect for x and y
            # Heuristic correct test for the classic editorial:
            xs = []
            ys = []
            for lo, hi in zip(anchors_low, anchors_high):
                if hi - lo <= 2 * d:
                    continue
                xs.append(lo + d)
                ys.append(hi - d)
            if not xs:
                return True
            return max(xs) <= min(ys)

        lo, hi = max(0, forced), 10 ** 9
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

# revisit: minor renames and one early exit added
