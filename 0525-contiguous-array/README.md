# 525. Contiguous Array

Difficulty: Medium
Topics  : array, hash table, prefix sum

## Problem

Given a binary array `nums`, return the length of the longest contiguous subarray containing an equal number of `0`s and `1`s.

## Approach

The trick is a relabeling: treat every `0` as `-1`. A subarray then has equal counts exactly when its elements sum to zero, and a zero-sum subarray is the same thing as two prefix sums being equal. So the question becomes "how far apart can two identical running sums be", which is a hash map away.

Walk the array keeping a running sum. If the sum has been seen before at index `j`, the slice `(j, i]` nets to zero and is a candidate of length `i - j`. If it has not, record the current index. Seeding the map with `{0: -1}` handles the case where the balanced stretch starts at index 0.

The one detail that decides correctness is storing only the *first* index for each sum and never overwriting it. Overwriting would shrink every future window, so the earliest occurrence is what makes each match maximal.

Same prefix-sum-plus-hash-map skeleton as 560, except 560 counts subarrays hitting a target and this one maximizes a length, so this version keeps first indices where 560 keeps frequencies.

## Complexity

Time O(n), space O(n) for the map.

## Files

- `python/solution.py`
