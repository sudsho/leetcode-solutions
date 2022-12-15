# 301. Remove Invalid Parentheses

Difficulty: Hard
Topics  : bfs, backtracking

## Problem

Remove minimum invalid parentheses to make a string valid. Return all unique results.

## Approach

Compute extra '(' and ')' to remove. Backtrack with index, skipping duplicates.

## Complexity

Time O(2^N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
