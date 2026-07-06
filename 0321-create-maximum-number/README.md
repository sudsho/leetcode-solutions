# 321. Create Maximum Number

Difficulty: Hard
Topics  : stack, greedy, monotonic stack, array

## Problem

Given two integer arrays `nums1` and `nums2` of single digits and an integer `k`,
create the maximum number of length `k` using digits from the two arrays. The
relative order of digits within each array must be preserved. Return the answer
as a length-`k` digit array.

## Approach

For each split `i` (take `i` digits from `nums1`, `k - i` from `nums2`):

1. `_pick` selects the maximum-value subsequence of the required length from one
   array using a monotonic stack (pop smaller trailing digits while enough remain).
2. `_merge` interleaves the two picks into the largest number, breaking ties by
   comparing the remaining suffixes lexicographically.

Take the best candidate over all valid splits.

## Complexity

Time O(k * (n + m + k)) over the O(k) splits, space O(k).

## Files

- `python/solution.py`
