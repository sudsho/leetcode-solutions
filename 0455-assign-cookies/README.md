# 455. Assign Cookies

Difficulty: Easy
Topics: greedy, sorting, two pointers

## Problem

Each child i has a greed factor `g[i]` (min cookie size to be content); each cookie j
has size `s[j]`. A cookie serves at most one child. Maximize the number of content children.

## Approach

Sort both arrays. Sweep with two pointers, giving the current child the smallest cookie
that meets their greed. If a cookie is too small for the current (least greedy remaining)
child it is too small for everyone left, so we discard it and move on.

## Complexity

Time O(n log n + m log m) for the sorts, space O(1) beyond sorting.

## Files

- `python/solution.py`
