# 1751. Maximum Number of Events That Can Be Attended II

Difficulty: Hard
Topics  : dp, binary search

## Problem

Pick at most k non-overlapping events to maximize sum of values.

## Approach

Sort by end. dp[i][j] = best using first i events with at most j picks. Binary search the latest non-overlapping.

## Complexity

Time O(NK log N), space O(NK).

## Files

- `python/solution.py`
- `python/solution_alt.py`
