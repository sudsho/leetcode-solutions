# 25. Reverse Nodes in k Group

Difficulty: Hard
Topics  : linked list, recursion

## Problem

Reverse the nodes of a linked list k at a time and return the modified list. Nodes left over at the end stay in original order.

## Approach

Walk forward k steps to verify a full group exists, then reverse that segment iteratively. Recurse on the rest.

## Complexity

Time O(N), space O(N/k) due to recursion (or O(1) iterative).

## Files

- `python/solution.py`
