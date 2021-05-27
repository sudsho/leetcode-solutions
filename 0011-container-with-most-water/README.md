# 11. Container With Most Water

Difficulty: Medium
Topics  : array, two pointers, greedy

## Problem

Given n non-negative integers, find two lines that together with the x-axis form a container which holds the most water.

## Approach

Two pointers from both ends. Width shrinks as we move in, so we move whichever side is shorter (the only one that could possibly improve).

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`

<!-- revisit -->
