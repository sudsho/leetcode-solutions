# 60. Permutation Sequence

Difficulty: Hard
Topics  : math, combinatorics

## Problem

Given n and k, return the kth permutation sequence of [1..n] in lexicographic order.

## Approach

Use factorial number system. Pick the first digit by k // (n-1)!, decrement, recurse.

## Complexity

Time O(N^2) due to list pop, space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
