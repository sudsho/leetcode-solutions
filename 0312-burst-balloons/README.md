# 312. Burst Balloons

Difficulty: Hard
Topics  : array, dp, interval dp

## Problem

Maximize coins by bursting balloons; bursting i gives nums[i-1]*nums[i]*nums[i+1].

## Approach

Interval DP. dp[l][r] = max coins from open interval (l, r). Loop over which balloon is burst LAST.

## Complexity

Time O(n^3), space O(n^2).

## Files

- `python/solution.py`
