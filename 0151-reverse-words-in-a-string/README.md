# 151. Reverse Words in a String

Difficulty: Medium
Topics: string, two pointers

## Problem

Given an input string s, reverse the order of the words. A word is a maximal run of non-space characters. Collapse multiple spaces and strip leading/trailing spaces so the result has words separated by a single space.

## Approach

`s.split()` with no separator splits on any whitespace and discards empty tokens, which handles the multiple-space and leading/trailing cases for free. Reverse the token list and re-join with one space.

## Complexity

Time O(n), space O(n) for the token list and output.

## Files

- `python/solution.py`
