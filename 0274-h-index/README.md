# 274. H-Index

Difficulty: Medium
Topics  : array, counting sort, sorting

## Problem

Given an array `citations` where `citations[i]` is the citation count of the i-th paper, return the researcher's h-index: the largest `h` such that at least `h` papers have `h` or more citations each.

## Approach

Two ways. Sorting descending, the h-index is the last rank `i` (1-based) where the paper still has `>= i` citations. That's O(n log n).

The counting-sort version is O(n): an h-index can never exceed `n`, so bucket every citation count with anything above `n` clamped into bucket `n`. Then sweep `h` from `n` down to `0` accumulating how many papers have at least `h` citations; the first `h` where that running total reaches `h` is the answer.

## Complexity

Counting version time O(n), space O(n). Sorting version time O(n log n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
