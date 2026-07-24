# 296. Best Meeting Point

Difficulty: Hard
Topics  : array, math, sorting

## Problem

A group of people live in a binary `grid`, where a `1` marks a home. Find the minimum total travel distance to a single meeting point, using Manhattan distance.

## Approach

Manhattan distance splits cleanly into an independent row term and column term, so the 2-D problem is two 1-D problems added together. In 1-D the total `sum |x - p|` is minimized when `p` is the median of the coordinates.

Collect the row and column indices of every home. Rows come out already sorted (outer loop is top-to-bottom); sort the columns. Then instead of naming the median, pair the coordinates from both ends inward — each pair straddles the median, so its span is its exact contribution, and the pairwise spans sum to the optimal cost.

`solution_alt.py` keeps the more literal version: take the median coordinate directly and sum absolute deviations.

## Complexity

Time O(m·n) to scan the grid plus O(k log k) to sort the columns (k homes); space O(k).

## Files

- `python/solution.py`
- `python/solution_alt.py`
