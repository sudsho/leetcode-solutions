# 1632. Rank Transform of a Matrix

Difficulty: Hard
Topics  : union find, sorting

## Problem

Replace each entry with its rank, where rank counts both row and column constraints.

## Approach

Group cells by value. For each value, union same-row and same-col cells. Each component's rank = 1 + max(row_rank, col_rank).

## Complexity

Time O(RC log RC), space O(RC).

## Files

- `python/solution.py`
- `python/solution_alt.py`
