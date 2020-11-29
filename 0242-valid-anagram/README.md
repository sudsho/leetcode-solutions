# 242. Valid Anagram

Difficulty: Easy
Topics: string, hash table

## Problem

Decide whether two strings are anagrams of each other (same letters, same counts).

## Approach

Count letters of one string, decrement for the other. If all counts end at zero, anagram. Or just compare sorted strings.

<!-- updated -->
## Complexity

Time O(n), space O(1) (alphabet size).

## Files

- `python/solution.py`
- `python/solution_alt.py`
