from collections import defaultdict


class Solution:
    def subarraysDivByK(self, nums, k):
        # same reduction as 523: a slice (j, i] is divisible by k exactly when
        # prefix[i] and prefix[j] agree mod k, because the multiples of k cancel
        # in the subtraction. the difference is the question - 523 asks whether
        # any such pair exists, this one asks how many, so the map stores
        # FREQUENCIES rather than first indices.
        counts = defaultdict(int)
        counts[0] = 1  # the empty prefix, so a prefix that is itself divisible counts
        running = 0
        total = 0
        for v in nums:
            # python's % already returns a non-negative result for a positive
            # modulus, so -3 % 5 == 2 and negative numbers need no fixup here.
            # in a language with truncated division this line is where the bug
            # lives: ((running % k) + k) % k.
            running = (running + v) % k
            # every earlier prefix with this same remainder closes a divisible
            # subarray ending at the current index.
            total += counts[running]
            counts[running] += 1
        return total


class SolutionArray:
    """Same counting with a fixed-size array instead of a dict.

    There are only k possible remainders, so the map can be a list of length k.
    Slightly faster in practice and it makes the O(k) space bound explicit.
    """

    def subarraysDivByK(self, nums, k):
        counts = [0] * k
        counts[0] = 1
        running = 0
        total = 0
        for v in nums:
            running = (running + v) % k
            total += counts[running]
            counts[running] += 1
        return total


class SolutionPairwise:
    """Count pairs at the end rather than incrementally - the n-choose-2 view.

    Any two prefixes sharing a remainder define a divisible slice, so the answer
    is the sum of C(c, 2) over the remainder buckets. Counting as we go and
    counting at the end give the same number; this version just makes it obvious
    that the answer only depends on the bucket sizes, not on the order.
    """

    def subarraysDivByK(self, nums, k):
        counts = [0] * k
        counts[0] = 1
        running = 0
        for v in nums:
            running = (running + v) % k
            counts[running] += 1
        return sum(c * (c - 1) // 2 for c in counts)
