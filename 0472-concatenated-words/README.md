# 472. Concatenated Words

Difficulty: Hard
Topics  : string, dp, trie

## Problem

Find words made up of two or more shorter words from the input.

## Approach

Sort by length. For each word, DP on prefixes against a set of shorter ones.

## Complexity

Time O(N * L^2), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
