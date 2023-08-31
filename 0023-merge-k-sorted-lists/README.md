# 23. Merge k Sorted Lists

Difficulty: Hard
Topics  : linked list, heap, divide and conquer

## Problem

Merge k sorted linked lists into one sorted list.

## Approach

Min heap keyed by node value, push each list head, pop smallest, push its successor.

## Complexity

Time O(N log k), space O(k).

## Files

- `python/solution.py`
- `python/solution_alt.py`
