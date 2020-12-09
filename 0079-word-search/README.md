# 79. Word Search

Difficulty: Medium
Topics  : array, backtracking, matrix

## Problem

Given a 2D board of letters and a word, return True if the word can be constructed from adjacent (4-dir) cells, no reuse.

## Approach

DFS with marking. Try every cell as a start. Marking the cell with a sentinel (we restore on backtrack) avoids needing a separate visited grid.

## Complexity

Time O(m*n*4^L), space O(L) recursion.

## Files

- `python/solution.py`
