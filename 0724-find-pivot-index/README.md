# 724. Find Pivot Index

Difficulty: Easy
Topics  : array, prefix sum

## Problem

Given an integer array `nums`, return the leftmost index `i` such that the sum of the elements strictly to the left of `i` equals the sum of the elements strictly to the right of `i`. Return `-1` if no such index exists. The empty side of an end index sums to zero.

## Approach

The naive read recomputes both sides at every index, which is O(n^2). The fix is the standard prefix-sum one: the right side is not independent information. Once the total is known, `right = total - left - nums[i]`, so a single running left sum decides the condition at every index in one pass.

That collapse means the prefix *array* is not needed either — only the running value. The explicit array version is kept as an alt because it is the same object 303 builds, and lining the two up makes the padding-zero convention obvious: `prefix[i]` is everything strictly left of `i`, which is exactly what the pivot condition asks for, so index 0 needs no branch.

Two details are worth pinning down. The comparison has to happen *before* absorbing `nums[i]` into the running sum, since the pivot element belongs to neither side. And negative values are allowed, so the sums are not monotonic and there is nothing to binary search on or prune with — the left-to-right scan is also what makes the answer the leftmost one for free.

## Complexity

Time O(n) for the pass, space O(1) for the running-sum version and O(n) for the explicit prefix array.

## Files

- `python/solution.py`
