# 128. Longest Consecutive Sequence

Difficulty: Medium
Topics  : array, hash table, union find

## Problem

Given an unsorted array of ints return the length of the longest consecutive sequence. O(n).

## Approach

Put all in a set. For each number that is the start of a run (i.e. n-1 not in set) walk forward.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
