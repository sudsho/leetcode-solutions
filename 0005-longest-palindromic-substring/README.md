# 5. Longest Palindromic Substring

Difficulty: Medium
Topics  : string, dynamic programming

## Problem

Given a string s, return the longest palindromic substring in s.

## Approach

Expand around each possible center. Each char (odd) and each gap between chars (even) is a center; expand while characters match.

## Complexity

Time O(n^2), space O(1).

## Files

- `python/solution.py`
