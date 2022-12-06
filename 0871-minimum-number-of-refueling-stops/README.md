# 871. Minimum Number of Refueling Stops

Difficulty: Hard
Topics  : heap, dp

## Problem

Min refueling stops to reach target. Greedy: pick max-fuel station among reachable.

## Approach

Max heap of station fuel. While current can't reach next, pop max.

## Complexity

Time O(N log N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
