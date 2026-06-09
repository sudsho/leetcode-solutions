# 90. Subsets II

Difficulty: Medium
Topics  : array, backtracking, bit manipulation

## Problem

Given an integer array that may contain duplicates, return all possible subsets
(the power set). The solution set must not contain duplicate subsets.

## Approach

Same backtracking skeleton as 78 (Subsets), but duplicates force one extra rule.
Sort the array first so equal values sit next to each other. At each recursion
depth we loop over the remaining candidates; the first time we reach a value at
this level we're free to pick it, but any later sibling with the same value would
generate a subset we've already produced, so we skip it. The `i > start` guard is
what distinguishes "first occurrence on this branch" from "duplicate sibling".

## Complexity

Time O(n * 2^n) - up to 2^n subsets, each costing O(n) to copy. Space O(n) for
the recursion path, ignoring the output.

## Files

- `python/solution.py`
