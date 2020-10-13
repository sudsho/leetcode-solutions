# 287. Find the Duplicate Number

Difficulty: Medium
Topics  : array, two pointers, binary search, bit manipulation

## Problem

Given an array of n+1 ints with values 1..n find the one duplicate. O(1) extra space, no mutation.

## Approach

Floyd's tortoise and hare on the implicit linked list defined by i -> nums[i].

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
