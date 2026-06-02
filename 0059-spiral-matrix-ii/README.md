# 59. Spiral Matrix II

Difficulty: Medium
Topics  : matrix, simulation

## Problem

Given n, fill an n by n matrix with the numbers 1..n*n in spiral order, starting from the top-left going clockwise.

## Approach

Four boundary pointers shrunk after each side is filled. The bottom row and left column need an extra guard for odd n where the spiral collapses into a single cell or row.

## Complexity

Time O(n^2), space O(n^2) for the output.

## Files

- `python/solution.py`
