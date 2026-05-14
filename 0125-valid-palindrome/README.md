# 125. Valid Palindrome

Difficulty: Easy
Topics  : two pointers, string

## Problem

Given a string, return true if it reads the same forward and backward after
removing non-alphanumeric characters and lowercasing.

## Approach

Two pointers from the two ends. Each step, skip any non-alphanumeric character
on either side, then compare lowercased characters. Bail out as soon as a
mismatch is found.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
