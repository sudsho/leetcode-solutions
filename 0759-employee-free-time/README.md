# 759. Employee Free Time

Difficulty: Hard
Topics  : heap, sweep

## Problem

Given each employee's working intervals, return the free intervals shared by all.

## Approach

Min heap on (start, employee, idx). Track current max end. New gap when next start > current end.

## Complexity

Time O(N log K), space O(K).

## Files

- `python/solution.py`
- `python/solution_alt.py`
