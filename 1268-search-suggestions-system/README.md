# 1268. Search Suggestions System

Difficulty: Medium
Topics  : string, trie, binary search

## Problem

For each prefix of searchWord return up to 3 lex-smallest products with that prefix.

## Approach

Sort products. For each prefix do bisect_left and take up to 3.

## Complexity

Time O(n log n + L * log n), space O(n).

## Files

- `python/solution.py`
