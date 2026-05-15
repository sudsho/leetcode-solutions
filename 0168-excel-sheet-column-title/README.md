# 168. Excel Sheet Column Title

Difficulty: Easy
Topics  : math, string

## Problem

Given a positive integer `n`, return its corresponding Excel column title (1 -> A, 26 -> Z, 27 -> AA, 28 -> AB, ...).

## Approach

Like base 26 but 1-indexed (no zero digit). At each step subtract 1 first so the
remainder lands in 0..25, then map to the letter and divide. Build the string
right to left and reverse at the end.

## Complexity

Time O(log_26 n), space O(log_26 n) for the output buffer.

## Files

- `python/solution.py`
