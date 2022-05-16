# 315. Count of Smaller Numbers After Self

Difficulty: Hard
Topics  : merge sort, BIT

## Problem

Count of nums[j] < nums[i] for j > i.

## Approach

Modified merge sort. During merge, count contributions when an element from right is placed before some from left.

## Complexity

Time O(N log N), space O(N).

## Files

- `python/solution.py`
