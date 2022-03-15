# 37. Sudoku Solver

Difficulty: Hard
Topics  : backtracking

## Problem

Fill a partially filled 9x9 sudoku board so each row, column and 3x3 box contains digits 1..9.

## Approach

Track used digits per row, column, box. Backtrack on empty cells.

## Complexity

Time worst-case exponential, space O(81).

## Files

- `python/solution.py`
- `python/solution_alt.py`
