# 719. Find K-th Smallest Pair Distance

Difficulty: Hard
Topics  : array, two pointers, binary search, sorting

## Problem

The distance of a pair `(a, b)` is `|a - b|`. Given an integer array `nums` and an integer `k`, return the `k`th smallest distance among all `n(n-1)/2` pairs `(nums[i], nums[j])` with `i < j`.

## Approach

Fourth problem on the same outer loop, picked to test yesterday's conclusion — that the shape is a monotone predicate and a bisect that finds its boundary, and everything past that is whatever answering the predicate takes. The predicate here is not a feasibility question. It counts. That turns out to change what the boundary *means*, which is the day.

The previous three all asked for the smallest `x` that could be done. "Can be done" was the question, so the answer being achievable was baked into the asking and never needed defending. This asks for an order statistic of a multiset — the `k`th smallest distance that actually occurs — and that multiset has `n(n-1)/2` elements and is never going to be built.

The bridge is one line. Let `c(x)` be the number of pairs at distance at most `x`. Then `c` is the cdf of the distance multiset, and the `k`th order statistic is exactly where that cdf first reaches `k` — so the answer is the smallest `x` with `c(x) >= k`, which is a boundary a bisect can find.

The gap that opens up is that the bisect ranges over every integer in `[0, max - min]`, and most of those are not distances between any two elements. So the boundary could a priori land on a value nothing realizes. It cannot, and this is the first day in four where that needed an argument: if `x` is minimal with `c(x) >= k` then `c(x - 1) < k`, so `c(x) > c(x - 1)`, so some pair sits at distance exactly `x`. The search space being too large is repaired for free by the boundary being a jump in `c`. First time the searched set has been strictly bigger than the set of possible answers, and it works because of a property of the predicate rather than a property of the range.

Two separate monotonicity claims are stacked in the counting pass and running them together cost the first version. The outer one is what the bisect needs: `c` is non-decreasing in the limit, since widening it only admits pairs. The inner one is what makes the pass linear: the left pointer never moves backwards as the right end advances, because the sorted value at the right only grew, so the smallest legal left index only grew too. Different claims about different variables, neither implying the other. "Monotone" had been reading as one property of the setup for three days.

Bounds again need no guard, third day running. `0` is a legal low even when no pair is at distance zero — it simply fails the predicate and the search moves off it. `max - min` is the largest distance in the multiset, so `c(high)` is `n(n-1)/2 >= k` and the range is nonempty. Both ends are read off the structure rather than picked large enough to be safe.

The witness alternate is the tenth day of the summary-versus-set split and non-canonical for the third distinct reason in four days. 1552's was symmetry, 2064's was slack, and this one is multiplicity — the answer *is* a value, and every pair separated by it realizes it equally. That is a stronger kind of non-canonical than the other two, which each had a canonical choice available if one had been wanted. Here there is no sense in which one pair is the witness, so the tests check the property and not the pair.

The heap alternate reads the distance multiset as `n - 1` already-sorted lists — for a fixed left index the distances ascend with the right index — and does a `k`-way merge, popping `k` times. Kept for the same reason as yesterday and it earns it better here: it shares no counting, no predicate, no monotonicity claim, and in particular no two-pointer sweep, which is the part of the primary least verifiable by inspection. A wrong-but-monotone `c` would produce a confident wrong boundary, so the sweep is also checked directly against its definition in the tests.

## Complexity

Primary: `O(n log n + n log W)` time where `W = max - min`, `O(1)` space beyond the sort. Heap: `O(n + k log n)`, fine for small `k` and hopeless as `k` approaches `n^2`, which is the honest reason it is an alternate. Witness: primary plus `O(n log n)`. Min-gap: `O(n log n)`.

## Files

- `python/solution.py`
