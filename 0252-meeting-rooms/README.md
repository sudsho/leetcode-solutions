# 252. Meeting Rooms

Difficulty: Easy
Topics  : array, sorting

## Problem

Given an array of meeting time intervals `[start, end]`, determine if a person could attend all meetings.

## Approach

Sort the intervals by start time. Once sorted, the only way to miss a meeting is for one to start before the previous one finishes, so scan adjacent pairs and fail on the first `cur.start < prev.end`. Touching endpoints (`cur.start == prev.end`) are fine since the earlier meeting has already ended.

## Complexity

Time O(n log n) for the sort, space O(1) beyond the sort.

## Files

- `python/solution.py`
