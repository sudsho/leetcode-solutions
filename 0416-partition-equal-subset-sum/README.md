# 416. Partition Equal Subset Sum

Difficulty: Medium
Topics  : array, dynamic programming

## Problem

Given an int array decide if it can be partitioned into two subsets with equal sum.

## Approach

If total is odd answer is no. Else 0/1 knapsack on target = total/2.

## Complexity

Time O(n*sum), space O(sum).

## Files

- `python/solution.py`
