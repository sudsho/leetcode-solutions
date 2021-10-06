# 31. Next Permutation

Difficulty: Medium
Topics  : array, two pointers

## Problem

Rearrange numbers to next lexicographic permutation.

## Approach

Find rightmost i with a[i]<a[i+1], swap a[i] with smallest larger element to its right, reverse suffix.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
