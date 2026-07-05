# 171. Excel Sheet Column Number

Difficulty: Easy
Topics  : math, string

## Problem

Given a string `columnTitle` as it appears on an Excel sheet (A, B, ..., Z, AA, AB, ...),
return its corresponding column number.

## Approach

The titles form a bijective base-26 system with digits A..Z = 1..26 and no zero.
Scan left to right, and for each character do `result = result * 26 + value(ch)`
where `value(ch) = ord(ch) - ord('A') + 1`.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
