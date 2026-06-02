# 86. Partition List

Difficulty: Medium
Topics  : linked list, two pointers

## Problem

Given a linked list and value x, reorder it so all nodes less than x come before nodes greater or equal to x. Preserve the original relative order in each group.

## Approach

Two dummy heads, one for the `< x` chain and one for the `>= x` chain. Walk the list once, append each node to the right chain, then stitch them together. The dummy heads remove the special-case for an empty group.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
