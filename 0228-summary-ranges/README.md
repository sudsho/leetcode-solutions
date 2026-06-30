# 228. Summary Ranges

Difficulty: Easy
Topics  : array + two pointers

## Problem

Given a sorted array of distinct integers, return the smallest sorted list of ranges that cover every number exactly once. A single number is written `"a"`, a run is written `"a->b"`.

## Approach

One linear scan. Fix the start of a run, extend while the next value is `prev + 1`, then emit the run and move on.

## Files

- `python/solution.py`
