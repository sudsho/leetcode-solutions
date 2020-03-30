# 146. LRU Cache

Difficulty: Medium
Topics  : design, hash table, linked list

## Problem

Design a data structure for least-recently-used cache with O(1) get and put.

## Approach

OrderedDict from collections supports move_to_end and popitem(last=False). With those, both ops are O(1) amortized.

## Complexity

Time O(1) per op, space O(capacity).

## Files

- `python/solution.py`
- `python/solution_alt.py`
