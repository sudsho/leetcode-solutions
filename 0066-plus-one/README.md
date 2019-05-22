# 66. Plus One

Difficulty: Easy
Topics: array, math

## Problem

Given a non-empty array of digits representing a non-negative integer, add 1 to it and return the result as a digit array.

## Approach

Walk from the right. Add carry. If digit becomes 10, set to 0 and carry on. If we walk off the front with carry, prepend a 1.

## Complexity

Time O(n), space O(1) (or O(n) if we prepend).

## Files

- `python/solution.py`
