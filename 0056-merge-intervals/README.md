# 56. Merge Intervals

Difficulty: Medium
Topics  : array, sorting

## Problem

Given intervals, merge all overlapping ones and return the result.

## Approach

Sort by start. Walk through; if the current overlaps the last in the result, extend the end; else append.

## Complexity

Time O(n log n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
