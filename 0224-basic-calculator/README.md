# 224. Basic Calculator

Difficulty: Hard
Topics  : stack, string

## Problem

Evaluate a string expression with +, -, parentheses, integers.

## Approach

Stack saves (sign, accumulated). Iterate; on '(' push, on ')' fold.

## Complexity

Time O(N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
