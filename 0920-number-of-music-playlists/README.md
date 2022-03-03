# 920. Number of Music Playlists

Difficulty: Hard
Topics  : dp

## Problem

Number of playlists of length goal using n songs with no song repeating until k other songs play.

## Approach

DP on (i, j) = playlists of length i with j unique songs. Transition: i-1, j-1 (new) or i-1, j (repeat with j-k options).

## Complexity

Time O(LN), space O(LN).

## Files

- `python/solution.py`
- `python/solution_alt.py`
