class Solution:
    def maxNumber(self, nums1, nums2, k):
        """Largest length-k number built from nums1 and nums2, keeping each
        array's relative order.

        The number splits cleanly: if we take exactly i digits from nums1 then we
        must take k - i from nums2, and the two chosen subsequences get merged.
        For a *fixed* i the two halves are independent, so the problem decomposes:

          1. pick the maximum-value subsequence of a given length from one array,
          2. merge two such subsequences into the largest interleaving,
          3. try every split i in [0..k] and keep the best result.

        `_pick` is a monotonic-stack greedy: walk the array keeping digits on a
        stack, popping smaller ones while enough remain to still fill `length` -
        this is the standard "remove digits to maximize" trick. `_merge` is the
        subtle part: when the two lead digits tie you cannot just pick either, you
        have to compare the *remaining sequences* lexicographically to decide
        which array to draw from, otherwise a later larger digit gets stranded.
        """

        def _pick(nums, length):
            """Max-value subsequence of exactly `length` digits, order preserved."""
            drop = len(nums) - length  # how many we're allowed to skip
            stack = []
            for d in nums:
                while drop and stack and stack[-1] < d:
                    stack.pop()
                    drop -= 1
                stack.append(d)
            return stack[:length]

        def _merge(a, b):
            """Interleave two digit lists into the largest number, keeping order."""
            merged = []
            while a or b:
                # comparing the lists directly breaks ties by looking ahead
                bigger = a if a > b else b
                merged.append(bigger[0])
                bigger.pop(0)
            return merged

        best = []
        # i digits from nums1, k - i from nums2; bounds keep both picks feasible
        for i in range(max(0, k - len(nums2)), min(k, len(nums1)) + 1):
            candidate = _merge(_pick(nums1, i), _pick(nums2, k - i))
            if candidate > best:
                best = candidate
        return best


if __name__ == "__main__":
    s = Solution()
    assert s.maxNumber([3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5) == [9, 8, 6, 5, 3]
    assert s.maxNumber([6, 7], [6, 0, 4], 5) == [6, 7, 6, 0, 4]
    assert s.maxNumber([3, 9], [8, 9], 3) == [9, 8, 9]
    assert s.maxNumber([5, 6, 8], [6, 4, 0], 3) == [8, 6, 4]
    print("all good")
