# 480. Sliding Window Median

Difficulty: Hard
Topics  : two heaps, sorted list

## Problem

Median of every window of size k as it slides over an array.

## Approach

Use SortedList for O(log k) insert / remove / index.

## Complexity

Time O(N log K), space O(K).

## Files

- `python/solution.py`
