# 384. Shuffle an Array

Difficulty: Medium
Topics: array, math, randomized

## Problem

Given an integer array, support two operations: `reset` returns the array to its original order, and `shuffle` returns a uniformly random permutation of it. Every permutation must be equally likely.

## Approach

Hold onto a copy of the original for `reset`. For `shuffle`, run Fisher-Yates: walk from the last index down to the first, and swap each element with a randomly chosen index at or before it. Because each pick draws from the still-unshuffled prefix, all n! orderings come out equally likely.

<!-- revisited -->
## Complexity

`shuffle` and `reset` are O(n) time, O(n) space for the stored copy.

## Files

- `python/solution.py`
