# 745. Prefix and Suffix Search

Difficulty: Hard
Topics  : trie

## Problem

Word filter; given a prefix and suffix, return the index of the most recent matching word.

## Approach

Build a trie keyed by suffix#word for every (suffix, word) pair. Search by suffix#prefix.

## Complexity

Time O(N * L^2) build, O(P+S) per query.

## Files

- `python/solution.py`
