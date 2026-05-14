# 80. Remove Duplicates From Sorted Array II

Difficulty: Medium
Topics  : array, two pointers

## Problem

Given a sorted array, remove duplicates in place so that each unique element
appears at most twice. Return the new length and keep the first `k` slots of
the array filled with the result.

## Approach

Single pass with a write pointer `k`. For each value we read, we copy it to
position `k` only if `k < 2` (room for the first two without checks) or if it
differs from the element two slots back. Because the input is sorted, this
guarantees no value appears more than twice in the output.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
