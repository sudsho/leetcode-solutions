# 354. Russian Doll Envelopes

Difficulty: Hard
Topics  : dp, binary search

## Problem

Find the largest chain of envelopes where each strictly fits in the next.

## Approach

Sort by w asc, h desc on tie. Then LIS on heights.

## Complexity

Time O(N log N), space O(N).

## Files

- `python/solution.py`
