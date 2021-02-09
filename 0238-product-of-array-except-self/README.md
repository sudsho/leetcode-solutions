# 238. Product of Array Except Self

Difficulty: Medium
Topics  : array, prefix sum

## Problem

Given an int array, return an array where each element is the product of all the others. No division. O(n) time.

## Approach

Two passes: first build prefix products into the output, then walk right-to-left multiplying by a running suffix product.

## Complexity

Time O(n), space O(1) extra.

## Files

- `python/solution.py`
- `python/solution_alt.py`
