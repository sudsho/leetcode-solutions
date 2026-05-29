# 57. Insert Interval

Difficulty: Medium
Topics  : array

## Problem

Given a list of non-overlapping intervals sorted by start, insert a new interval and merge any overlaps.

## Approach

Single linear pass in three phases: append intervals that end before the new one starts, absorb every interval that overlaps the new one into a single merged interval, then append the remainder. Input is already sorted so no extra O(n log n) sort step is needed.

## Complexity

Time O(n), space O(n) for the output.

## Files

- `python/solution.py`
