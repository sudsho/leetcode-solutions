# 253. Meeting Rooms II

Difficulty: Medium
Topics  : array, heap, sorting

## Problem

Given meeting time intervals, return the minimum number of conference rooms required.

## Approach

Sort by start time, use a min-heap of end times. For each meeting if the earliest-ending room is free reuse it, else add a new room.

## Complexity

Time O(n log n), space O(n).

## Files

- `python/solution.py`
