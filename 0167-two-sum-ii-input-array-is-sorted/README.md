# 167. Two Sum II - Input Array Is Sorted

Difficulty: Easy
Topics  : two pointers, binary search

## Problem

Given a 1-indexed array of integers sorted in non-decreasing order, find two numbers that add up to a specific target. Return the indices (1-based) of the two numbers.

## Approach

Two pointers from both ends. If the sum is too small bump the left pointer up, if too large pull the right pointer in. Sorted order makes this O(n) with no extra hashmap needed.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
