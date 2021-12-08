# 494. Target Sum

Difficulty: Medium
Topics  : dp, knapsack

## Problem

Number of expressions that evaluate to target by assigning + or - to each number.

## Approach

Reduce to subset-sum: find subsets summing to (sum + target) / 2.

## Complexity

Time O(n * S), space O(S).

## Files

- `python/solution.py`
