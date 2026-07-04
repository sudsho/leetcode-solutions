# 179. Largest Number

Difficulty: Medium
Topics: array, string, greedy, sorting, comparator

## Problem

Given a list of non-negative integers, arrange them so that concatenating them
in order forms the largest possible number. Return it as a string.

## Approach

Sorting by numeric value fails (`[3, 30]` must give `"330"`). Instead sort the
string forms with a pairwise comparator: `a` comes before `b` when `a + b > b + a`.
That comparator defines a valid total order, so a single sort produces the optimal
arrangement. Guard the all-zeros case so the result is `"0"` rather than `"00"`.

## Complexity

Time O(n log n) comparisons, each an O(k) string concat where k is the max digit
length; space O(n) for the string copies.

## Files

- `python/solution.py`
