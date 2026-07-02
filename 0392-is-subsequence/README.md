# 392. Is Subsequence

Difficulty: Easy
Topics: two pointers, string, dynamic programming

## Problem

Given strings s and t, return whether s is a subsequence of t. A subsequence keeps the relative order of characters but may drop some of them.

## Approach

Two pointers. Walk j across t; every time t[j] matches the next needed char s[i], advance i. s is a subsequence exactly when i reaches len(s).

If there were many queries s against the same t, preprocess t into per-character sorted index lists and binary-search the next position instead (see the follow-up alt solution).

## Complexity

Time O(len(t)), space O(1).

## Files

- `python/solution.py`
