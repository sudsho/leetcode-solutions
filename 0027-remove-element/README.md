# 27. Remove Element

Difficulty: Easy
Topics: array, two pointers

## Problem

Given an array and a value val, remove all instances of val in place and return the new length. The order of the kept elements does not matter.

## Approach

Slow pointer marks next slot for kept values. Walk fast through the array, copy to slow only when value differs from val.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
