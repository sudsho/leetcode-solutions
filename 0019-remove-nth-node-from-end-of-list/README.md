# 19. Remove Nth Node From End of List

Difficulty: Medium
Topics  : linked list, two pointers

## Problem

Given the head of a linked list, remove the nth node from the end and return the head.

## Approach

Two pointers. Move fast n steps ahead, then move both until fast hits the end. Slow now sits just before the node to remove.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
