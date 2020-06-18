# 3. Longest Substring Without Repeating Characters

Difficulty: Medium
Topics  : string, sliding window, hash table

## Problem

Given a string s, find the length of the longest substring without repeating characters.

## Approach

Sliding window with a dict that maps each char to its last index. When we hit a duplicate inside the window, jump the left pointer just past the previous occurrence.

## Complexity

Time O(n), space O(min(n, alphabet)).

## Files

- `python/solution.py`
- `python/solution_alt.py`
