# 12. Integer To Roman

Difficulty: Medium
Topics  : math, string, greedy

## Problem

Convert an integer in the range 1..3999 to its Roman numeral representation.

## Approach

Greedy with a fixed table of value/symbol pairs that already includes the six subtractive forms (CM, CD, XC, XL, IX, IV). Walk from largest to smallest and subtract while it still fits. Including the subtractive entries up front means we never need to look back and rewrite output.

## Complexity

Time O(1) since the integer is bounded by 3999. Space O(1).

## Files

- `python/solution.py`
