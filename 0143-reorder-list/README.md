# 143. Reorder List

Difficulty: Medium
Topics: linked list, two pointers, recursion

## Problem

Given the head of a singly linked list L0->L1->...->Ln-1->Ln, reorder it to
L0->Ln->L1->Ln-1->L2->Ln-2->... You may not modify the values, only the node
links.

## Approach

Split the list at its midpoint (slow/fast pointers), reverse the second half in
place, then merge the two halves by alternating nodes. No extra storage beyond
a few pointers.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
