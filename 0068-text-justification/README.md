# 68. Text Justification

Difficulty: Hard
Topics  : string, simulation

## Problem

Given a list of words and a maxWidth, format text so each line has exactly maxWidth chars, fully justified.

## Approach

Greedy pack words into a line. Distribute spaces left to right; last line is left-justified.

## Complexity

Time O(N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
