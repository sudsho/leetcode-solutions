# 1. Two Sum

Difficulty: Easy
Topics  : array, hash table

## Problem

Given a list of integers and a target value, return indices of two numbers that add up to the target. Each input has exactly one solution and we cannot use the same element twice.

## Approach

Walk the array once and keep a dict mapping each value seen so far to its index. For every new number, check if target minus that number is already in the dict. If so, we have our pair.

<!-- revisited -->
## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
