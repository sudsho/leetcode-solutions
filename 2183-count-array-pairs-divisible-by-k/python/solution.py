from typing import List
from math import gcd


class Solution:
    def countPairs(self, nums: List[int], k: int) -> int:
        # the predicate is k | nums[i] * nums[j], and it factors through
        # x |-> gcd(x, k):
        #
        #   k | nums[i]*nums[j]  <=>  k | gcd(nums[i],k) * gcd(nums[j],k)
        #
        # (<=) gcd(a,k) | a and gcd(b,k) | b, so their product divides a*b.
        # (=>) per prime, with p^e || k, p^s || a, p^t || b. the hypothesis is
        #      s + t >= e and the claim is min(s,e) + min(t,e) >= e. if s >= e
        #      the first term alone is e; same for t; otherwise both mins are s
        #      and t and the sum is untouched.
        #
        # so the whole array can be replaced by its image in the divisors of k
        # before anything is counted. that image is small - d(k) <= 128 for
        # k <= 1e5 - and it is the *coarsest* map the predicate factors through,
        # because distinct divisors g != g' are separated by an explicit witness:
        # k//g pairs with g and not with g' when g doesn't divide g', and k//g'
        # does the reverse otherwise.
        counts = {}
        for x in nums:
            g = gcd(x, k)
            counts[g] = counts.get(g, 0) + 1

        # now count pairs of classes rather than pairs of elements. O(d(k)^2)
        # with d(k) <= 128, so ~16k tests regardless of n.
        classes = sorted(counts)
        total = 0
        for i, a in enumerate(classes):
            ca = counts[a]
            if a * a % k == 0:
                # both endpoints in the same class: unordered pairs within it
                total += ca * (ca - 1) // 2
            for b in classes[i + 1:]:
                if a * b % k == 0:
                    total += ca * counts[b]
        return total
