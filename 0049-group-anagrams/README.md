# 49. Group Anagrams

Difficulty: Medium
Topics  : string, hash table, sorting

## Problem

Given an array of strings group the anagrams together.

## Approach

Bucket by sorted-string key, or by 26-letter count tuple.

## Complexity

Time O(n*k log k) sort version, space O(n*k).

## Files

- `python/solution.py`
