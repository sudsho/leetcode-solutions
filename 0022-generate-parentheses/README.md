# 22. Generate Parentheses

Difficulty: Medium
Topics  : string, dynamic programming, backtracking

## Problem

Given n pairs of parentheses, generate all combinations of well-formed parentheses.

## Approach

Backtracking. Track count of open and close used. Add `(` if open<n; add `)` only if close<open. Stop when length is 2n.

## Complexity

Time O(catalan(n)), space O(n) recursion.

## Files

- `python/solution.py`
- `python/solution_alt.py`
