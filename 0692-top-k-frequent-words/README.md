# 692. Top K Frequent Words

Difficulty: Medium
Topics  : hashmap, heap, trie, sorting

## Problem

Top k most frequent words, ties broken alphabetically.

## Approach

Count, push (count, word) into a heap of size k with negated count for stable order.

## Complexity

Time O(n log k), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
