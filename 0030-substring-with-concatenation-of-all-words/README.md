# 30. Substring with Concatenation of All Words

Difficulty: Hard
Topics  : hash map, sliding window

## Problem

Given a string s and a list of words of equal length, find all starting indices where the concatenation of all words appears.

## Approach

Sliding window of size word_len * len(words) but step by word_len from each offset 0..word_len-1. Track word counts.

## Complexity

Time O(N * word_len), space O(M).

## Files

- `python/solution.py`
- `python/solution_alt.py`
