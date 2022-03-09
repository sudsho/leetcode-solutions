# 460. Lfu Cache

Difficulty: Hard
Topics  : design, doubly linked list

## Problem

Implement LFU (least-frequently-used) cache with O(1) get and put.

## Approach

Two hashmaps. key -> (val, freq). freq -> ordered dict of keys at that frequency. Track min_freq.

## Complexity

Time O(1) per op, space O(capacity).

## Files

- `python/solution.py`
