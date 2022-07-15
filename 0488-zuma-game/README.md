# 488. Zuma Game

Difficulty: Hard
Topics  : backtracking, dfs

## Problem

Zuma-like puzzle. Insert balls into the row to clear groups of three or more.

## Approach

Recursive search. Try inserting each color of available hand into each gap, then collapse.

## Complexity

Time exponential in worst case.

## Files

- `python/solution.py`
