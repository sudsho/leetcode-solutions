# 20. Valid Parentheses

Difficulty: Easy
Topics: stack, string

## Problem

Decide if a string of (, ), {, }, [, ] is valid. Brackets must close in the correct order and every opening bracket needs a matching close.

## Approach

Use a stack. Push openings. When we see a close, pop and check it matches. End valid only if stack is empty.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
