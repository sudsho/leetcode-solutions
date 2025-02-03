# 234. Palindrome Linked List

Difficulty: Easy
Topics: linked list, two pointers

## Problem

Decide whether a singly linked list reads the same forward and backward.

## Approach

Easy approach: copy values to a list and compare with its reverse. Trickier O(1) extra space: find middle, reverse second half, compare.

## Complexity

Time O(n), space O(n) array version; O(1) reverse-half version.

## Files

- `python/solution.py`
- `python/solution_alt.py`
