# 258. Add Digits

Difficulty: Easy
Topics  : math, digital root

## Problem

Given a non-negative integer, repeatedly add all its digits until the result has only one digit, then return it. For example 38 -> 3 + 8 = 11 -> 1 + 1 = 2.

## Approach

The straightforward way is to loop: sum the digits, and repeat while the value is still two or more digits.

There is also a closed-form trick. The repeated digit sum is the digital root, which for a positive number cycles through 1..9 following `1 + (num - 1) % 9`, and is 0 only when the input is 0. That skips the loop entirely.

## Complexity

Loop version time O(log num) per fold, O(1) formula version. Space O(1) either way.

## Files

- `python/solution.py`
- `python/solution_alt.py`
