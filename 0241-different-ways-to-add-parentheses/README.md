# 241. Different Ways to Add Parentheses

Difficulty: Medium
Topics  : divide and conquer, dp

## Problem

Given an expression with numbers and ops, return all possible results from parenthesization.

## Approach

Split at each operator. Recurse on left and right. Combine.

## Complexity

Time exponential; cached to Catalan-ish.

## Files

- `python/solution.py`
