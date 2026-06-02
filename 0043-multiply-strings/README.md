# 43. Multiply Strings

Difficulty: Medium
Topics  : math, string, simulation

## Problem

Given two non-negative integers as strings, return their product as a string. No built-in big integer.

## Approach

Schoolbook multiplication into an `n + m` digit buffer. Position `i + j + 1` holds the units digit of `num1[i] * num2[j]`, carry goes one slot left. Walk i, j from the right, accumulate, then strip leading zeros at the end.

## Complexity

Time O(n * m), space O(n + m).

## Files

- `python/solution.py`
