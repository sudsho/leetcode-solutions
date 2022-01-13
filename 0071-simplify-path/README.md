# 71. Simplify Path

Difficulty: Medium
Topics  : stack, string

## Problem

Given a Unix-style absolute path, simplify it to its canonical form.

## Approach

Split on `/`. Stack: push valid name, pop on `..`, ignore `.` and empty.

## Complexity

Time O(N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
