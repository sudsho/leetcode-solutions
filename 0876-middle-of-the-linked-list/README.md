# 876. Middle of the Linked List

Difficulty: Easy
Topics: linked list, two pointers

## Problem

Return the middle node of a linked list. If even length, return the second middle.

## Approach

Slow and fast pointers. Slow moves 1, fast moves 2. When fast reaches the end, slow is at the middle.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
