# 299. Bulls and Cows

Difficulty: Medium
Topics  : hash map, counting

## Problem

Return string in form of xAyB representing bulls (correct position) and cows (right digit, wrong position).

## Approach

One pass count bulls; one pass tally per-digit counts; cows = sum of mins minus bulls.

## Complexity

Time O(N), space O(10).

## Files

- `python/solution.py`
- `python/solution_alt.py`
