# 763. Partition Labels

Difficulty: Medium
Topics  : greedy, two pointers, string

## Problem

Partition string so each letter appears in at most one part.

## Approach

Track last index per char, expand window until i hits the running max.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
