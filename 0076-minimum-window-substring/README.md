# 76. Minimum Window Substring

Difficulty: Hard
Topics  : string, sliding window, hashmap

## Problem

Smallest substring of s containing every char of t (with multiplicity).

## Approach

Sliding window with a counter, shrink while window is valid, track best.

## Complexity

Time O(n + m), space O(m).

## Files

- `python/solution.py`
- `python/solution_alt.py`
