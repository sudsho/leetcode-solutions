# 83. Remove Duplicates from Sorted List

Difficulty: Easy
Topics  : linked list

## Problem

Given the head of a sorted singly linked list, delete all nodes that have a duplicate value so each value appears only once. Return the head of the modified list.

## Approach

Because the list is already sorted, any duplicates sit next to each other. Walk the list with a single pointer. At every step compare the current node with its neighbour. If they match, splice the neighbour out by pointing `cur.next` past it and stay on the same `cur` so we can keep skipping a run of equal values. Otherwise advance.

## Complexity

Time O(n) with a single pass, space O(1) since we only rewire existing nodes.

## Files

- `python/solution.py`
