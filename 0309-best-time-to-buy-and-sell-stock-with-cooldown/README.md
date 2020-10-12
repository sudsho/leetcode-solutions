# 309. Best Time to Buy and Sell Stock with Cooldown

Difficulty: Medium
Topics  : array, dynamic programming

## Problem

Maximize profit with cooldown of 1 day after each sell.

## Approach

State machine: hold, sold, rest. Transitions update each from the previous step.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
