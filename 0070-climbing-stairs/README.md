# 70. Climbing Stairs

Difficulty: Easy
Topics: dynamic programming

## Problem

You climb a staircase with n steps and can take 1 or 2 steps at a time. Return the number of distinct ways to reach the top.

## Approach

Same recurrence as Fibonacci. ways(n) = ways(n-1) + ways(n-2). Use two variables instead of an array.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
