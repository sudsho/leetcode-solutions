# 282. Expression Add Operators

Difficulty: Hard
Topics  : backtracking

## Problem

Insert +, -, * between digits of a string so the expression equals target. Return all valid strings.

## Approach

Backtrack with running value and last operand (for *). Watch leading zeroes.

## Complexity

Time O(4^N), space O(N).

## Files

- `python/solution.py`
