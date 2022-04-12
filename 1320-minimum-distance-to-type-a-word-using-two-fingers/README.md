# 1320. Minimum Distance to Type a Word Using Two Fingers

Difficulty: Hard
Topics  : dp

## Problem

Type a word using two fingers; cost is sum of finger move distances.

## Approach

DP keyed by (position, finger1_loc, finger2_loc). Move one of the two fingers each step.

## Complexity

Time O(N * 27 * 27), space O(N * 27 * 27) compressed.

## Files

- `python/solution.py`
- `python/solution_alt.py`
