# 169. Majority Element

Difficulty: Easy
Topics: array, divide and conquer

## Problem

Given an array where one element appears more than n/2 times, return that majority element. Assume it always exists.

## Approach

Boyer-Moore voting. Track a candidate and a counter. Same as candidate -> count++, else count--. Reset candidate when count hits 0.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
