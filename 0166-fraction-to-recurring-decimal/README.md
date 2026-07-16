# 166. Fraction to Recurring Decimal

Difficulty: Medium
Topics: hash table, math, string

## Problem

Given two integers `numerator` and `denominator`, return the fraction as a
string. If the fractional part is repeating, enclose the repeating part in
parentheses. Any valid answer within 10^4 output length is accepted.

## Approach

Handle the sign up front, then do long division. The integer part is one
`divmod`. For the fractional part, keep pulling digits (remainder * 10 // d) and
record the output position each remainder first appears at. If a remainder
recurs, the digits since its first appearance are the repeating block, so insert
`(` at that stored position and append `)`. A zero remainder terminates.

## Complexity

Time O(k) where k is the length of the output (bounded by the number of distinct
remainders, at most `denominator`), space O(k) for the remainder map.

## Files

- `python/solution.py`
