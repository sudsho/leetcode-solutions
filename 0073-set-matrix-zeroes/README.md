# 73. Set Matrix Zeroes

Difficulty: Medium
Topics  : array, hash table, matrix

## Problem

Given an m x n matrix, if a cell is 0 set its entire row and column to 0. Do it in place.

## Approach

Use first row and column as markers. Track separately whether the first row/col themselves contain a zero.

## Complexity

Time O(m*n), space O(1).

## Files

- `python/solution.py`
