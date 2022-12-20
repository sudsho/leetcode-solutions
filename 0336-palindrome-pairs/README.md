# 336. Palindrome Pairs

Difficulty: Hard
Topics  : trie, hash map

## Problem

Find all index pairs (i, j) where words[i] + words[j] is a palindrome.

## Approach

Reverse-word lookup. For each word and each split, check if the reversed prefix or suffix is a palindrome.

## Complexity

Time O(N * L^2), space O(N * L).

## Files

- `python/solution.py`
