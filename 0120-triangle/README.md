# 120. Triangle

Difficulty: Medium
Topics: array, dynamic programming

## Problem

Given a triangle array, return the minimum path sum from top to bottom. From index j on one row you may step to index j or j+1 on the row below.

## Approach

Bottom-up DP over a single row buffer initialised to the last triangle row. Fold each higher row in: dp[j] = triangle[i][j] + min(dp[j], dp[j+1]). The minimum total ends up in dp[0].

## Complexity

Time O(n^2) over the triangle entries, space O(n) for the rolling row.

## Files

- `python/solution.py`
