# 316. Remove Duplicate Letters

Difficulty: Medium
Topics: string, stack, greedy, monotonic stack

## Problem

Remove duplicate letters so every letter appears once and the result is the smallest in lexicographical order among all such subsequences.

## Approach

Greedy monotonic stack. Precompute each letter's last index. Scan left to right; skip letters already on the stack. Before pushing, pop any greater top that still appears later, so smaller letters bubble forward without losing any character.

## Complexity

Time O(n), space O(1) (stack and sets bounded by the 26-letter alphabet).

## Files

- `python/solution.py`
