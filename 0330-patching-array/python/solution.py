class Solution:
    def minPatches(self, nums, n):
        """Minimum patches so every value in [1, n] is a subset sum of nums.

        Greedy on reachability. Keep `miss`, the smallest amount in [1, n]
        that we cannot yet form. If the current array element is <= miss it
        only extends what we can reach, so fold it in: miss += nums[i]. Once
        every available element is too large (or exhausted) we must patch,
        and the best patch is `miss` itself, which doubles the reach to
        [1, 2*miss - 1]. Stop as soon as miss exceeds n.
        """
        patches = 0
        miss = 1  # smallest sum in [1, n] we cannot currently build
        i = 0
        while miss <= n:
            if i < len(nums) and nums[i] <= miss:
                miss += nums[i]  # element fits, extends coverage for free
                i += 1
            else:
                miss += miss  # patch with `miss`, doubling the reachable range
                patches += 1
        return patches


if __name__ == "__main__":
    s = Solution()
    assert s.minPatches([1, 3], 6) == 1      # add 2 -> covers 1..6
    assert s.minPatches([1, 5, 10], 20) == 2  # add 2 and 4
    assert s.minPatches([1, 2, 2], 5) == 0
    print("all good")
