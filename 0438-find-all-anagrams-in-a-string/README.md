# 438. Find All Anagrams in a String

Difficulty: Medium
Topics: string, sliding window, hash table

## Problem

Given strings `s` and `p`, return the start indices of every substring of `s` that is an anagram of `p`.

## Approach

Fixed-width sliding window of length `len(p)`. Hold a 26-length frequency table for the window and one for `p`. Rather than re-comparing the whole table each step, track how many of the 26 letters currently match the target and only update the two letters that change as the window slides. The window is an anagram exactly when all 26 letters match.

## Complexity

Time O(n), space O(1) (two fixed 26-length tables).

## Files

- `python/solution.py`
- `python/solution_alt.py`
