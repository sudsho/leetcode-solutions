# 268. Missing Number

Difficulty: Easy
Topics: math, bit manipulation, array

## Problem

Given an array containing n distinct numbers from 0 to n, return the one missing.

## Approach

Sum 0..n is n*(n+1)/2. Subtract sum of array. The difference is the missing value.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
