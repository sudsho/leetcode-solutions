# 493. Reverse Pairs

Difficulty: Hard
Topics: array, divide and conquer, binary indexed tree, merge sort

## Problem

Given an integer array `nums`, return the number of reverse pairs. A reverse pair is a pair `(i, j)` where `0 <= i < j < nums.length` and `nums[i] > 2 * nums[j]`.

## Approach

Merge sort. On each merge, both halves are already sorted, so count the pairs with a two-pointer sweep before merging: for each left value, advance a pointer over the right half while it still dominates `2 * right`. The pointer only moves forward across the whole left scan, so counting stays O(n) per level.

The `> 2 * right` test does not line up with the merge comparison itself, which is why the count is a separate sweep rather than being folded into the merge like in 315.

## Complexity

Time O(n log n), space O(n).

## Files

- `python/solution.py` — merge sort with a two-pointer count per level
- `python/solution_alt.py` — Fenwick tree with coordinate compression
