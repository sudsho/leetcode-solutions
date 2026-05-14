# 164. Maximum Gap

Difficulty: Hard
Topics  : bucket sort, radix sort, math

## Problem

Given an unsorted array, return the maximum difference between two successive
elements in its sorted form. Required to run in linear time and linear extra
space, so the comparison sort O(n log n) approach is technically off the table.

## Approach

Bucket sort with the pigeonhole argument. If `n` numbers lie in `[lo, hi]`,
the maximum gap is at least `ceil((hi - lo) / (n - 1))`. Choose that value as
the bucket width and there will be at least one empty bucket if the values
aren't uniformly spaced. Because of that, the largest gap must cross between
two adjacent non-empty buckets - not be inside one. We only need to track each
bucket's min and max, then sweep left to right comparing each non-empty
bucket's min to the previous non-empty bucket's max.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
