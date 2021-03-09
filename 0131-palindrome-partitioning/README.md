# 131. Palindrome Partitioning

Difficulty: Medium
Topics  : string, backtracking, dp

## Problem

Partition s into substrings, each a palindrome, return all such partitionings.

## Approach

Backtracking. For each position try every prefix and recurse if palindrome.

## Complexity

Time O(n * 2^n), space O(n).

## Files

- `python/solution.py`
