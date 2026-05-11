# 58. Length of Last Word

Difficulty: Easy
Topics  : string

## Problem

Given a string consisting of words and spaces, return the length of the last word in the string. A word is a maximal substring of non-space characters.

## Approach

Scan from the right edge of the string. First skip any trailing spaces, then count characters until we hit another space or run out of string. This avoids splitting and allocates no extra memory.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
