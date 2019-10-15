# 387. First Unique Character in a String

Difficulty: Easy
Topics: string, hash table

## Problem

Find the index of the first character that does not repeat in the string. Return -1 if there is no such character.

## Approach

First pass counts occurrences. Second pass returns the first index whose count is 1.

## Complexity

Time O(n), space O(1) (alphabet size).

## Files

- `python/solution.py`
