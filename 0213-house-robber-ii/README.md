# 213. House Robber Ii

Difficulty: Medium
Topics  : dp

## Problem

House Robber but houses are arranged in a circle.

## Approach

Run linear House Robber on nums[1:] and nums[:-1], return max.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
