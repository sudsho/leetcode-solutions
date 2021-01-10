# 32. Longest Valid Parentheses

Difficulty: Hard
Topics  : string, dp, stack

## Problem

Find the length of the longest valid parentheses substring.

## Approach

Stack of indices. Push -1 sentinel, push '(' indices, on ')' pop and compute width.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
