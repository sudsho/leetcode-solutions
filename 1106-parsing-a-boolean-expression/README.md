# 1106. Parsing a Boolean Expression

Difficulty: Hard
Topics  : stack, recursion

## Problem

Parse and evaluate a boolean expression with !, &, | and t/f.

## Approach

Stack-based parse, fold each ')' by popping operands until matching operator.

## Complexity

Time O(N), space O(N).

## Files

- `python/solution.py`
