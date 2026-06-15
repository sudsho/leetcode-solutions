# 330. Patching Array

Difficulty: Hard
Topics: array, greedy

## Problem

Given a sorted array `nums` and an integer `n`, add (patch) the fewest possible
elements so that every value in the range `[1, n]` can be written as the sum of
some subset of the array. Return the minimum number of patches needed.

## Approach

Greedy on the reachable prefix. Track `miss`, the smallest value in `[1, n]`
that the current elements cannot form yet. Whenever the next array element is
at most `miss`, it only widens the reachable range without leaving a gap, so we
absorb it (`miss += nums[i]`). When no usable element is available, the optimal
patch is `miss` itself: adding it shifts the reachable range from `[1, miss-1]`
to `[1, 2*miss - 1]`, the largest jump a single patch can buy. We stop once
`miss > n`.

## Complexity

Time O(m + log n) where m is the length of `nums`: each array element is used
once, and the doubling patches add at most a logarithmic number of steps.
Space O(1).

## Files

- `python/solution.py`
