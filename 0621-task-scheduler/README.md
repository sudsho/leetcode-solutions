# 621. Task Scheduler

Difficulty: Medium
Topics  : heap, greedy, math

## Problem

Min total time to schedule tasks with cooldown n.

## Approach

Math: max_count * (n+1) + ties, lower-bounded by len(tasks).

## Complexity

Time O(t), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
