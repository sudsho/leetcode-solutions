# 451. Sort Characters By Frequency

Difficulty: Medium
Topics: hash table, string, bucket sort, heap

## Problem

Given a string s, sort its characters in decreasing order of frequency and return the resulting string. Characters with the same frequency may appear in any order.

## Approach

Count characters with a hash map, then bucket them by frequency (index = count). Reading buckets from highest count to lowest and emitting `char * count` yields the answer in linear time, avoiding a comparison sort of the distinct characters.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
