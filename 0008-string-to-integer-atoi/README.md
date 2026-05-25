# 8. String To Integer (Atoi)

Difficulty: Medium
Topics  : string, parsing

## Problem

Convert a string to a 32-bit signed integer, mimicking the classic C atoi. Skip leading whitespace, optional sign, then read digits until a non-digit. Clamp the result to the 32-bit signed range.

## Approach

Walk an index pointer through four phases: whitespace, optional sign, digit accumulation, stop. Clamp inside the digit loop so very long inputs cannot blow up `result`.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
