# 41. First Missing Positive

Difficulty: Hard
Topics  : array, in-place hashing

## Problem

Smallest positive integer missing from an unsorted array, O(n) time and O(1) space.

## Approach

Use the array itself as a hash. Place each n in the slot at index n-1. Scan for first slot where a[i] != i+1.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
