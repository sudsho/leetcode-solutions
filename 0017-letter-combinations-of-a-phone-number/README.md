# 17. Letter Combinations of a Phone Number

Difficulty: Medium
Topics  : string, backtracking

## Problem

Given a string of digits 2-9 return all possible letter combinations the number could represent.

## Approach

Backtracking. For each digit, try each letter and recurse. Iterative cross product also works.

## Complexity

Time O(4^n * n), space O(n) recursion.

## Files

- `python/solution.py`
