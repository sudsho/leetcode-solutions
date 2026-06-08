# 150. Evaluate Reverse Polish Notation

Difficulty: Medium
Topics: array, math, stack

## Problem

Given an array of tokens representing an arithmetic expression in Reverse Polish Notation, evaluate it and return the integer result. Valid operators are `+`, `-`, `*`, and `/`. Division between two integers truncates toward zero. The expression is always valid.

## Approach

RPN is built to be read with a stack. Walk the tokens left to right: a number gets pushed, an operator pops its two operands (the second popped is the left operand), applies itself, and pushes the result. After the scan a single value remains, the answer. The only subtlety is division: the problem wants truncation toward zero, so use `int(a / b)` rather than `//`, which floors and would round the wrong way for negative results.

## Complexity

Time O(n), space O(n) for the stack.

## Files

- `python/solution.py`
