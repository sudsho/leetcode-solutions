# 231. Power of Two

Difficulty: Easy
Topics: bit manipulation, math

## Problem

Decide whether a positive integer n is a power of two.

## Approach

A power of two has exactly one set bit. n & (n - 1) clears the lowest set bit; if the result is 0 and n > 0 then n is a power of two.

## Complexity

Time O(1), space O(1).

## Files

- `python/solution.py`
