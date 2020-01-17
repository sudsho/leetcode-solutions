# 215. Kth Largest Element in an Array

Difficulty: Medium
Topics  : array, divide and conquer, heap, quickselect

## Problem

Find the kth largest element in an unsorted array.

## Approach

Min-heap of size k; smallest in the heap at the end is the kth largest. Quickselect would be O(n) average.

## Complexity

Time O(n log k), space O(k).

## Files

- `python/solution.py`
- `python/solution_alt.py`
