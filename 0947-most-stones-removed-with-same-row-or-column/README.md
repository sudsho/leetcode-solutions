# 947. Most Stones Removed With Same Row Or Column

Difficulty: Medium
Topics  : Union-find + an answer that is a quotient invariant

## Problem

A stone may be removed if it shares a row or a column with a stone still on the
board. Return the maximum number removable.

## Approach

`n - c` for `c` the number of connected components of "shares a row or column".
The upper bound is an invariant rather than an exchange argument - the last
survivor of a component has nothing left to share with, so no component can be
emptied. The lower bound is a spanning tree peeled from the leaves inward, and
its root is free, so each component has `k` distinct optimal plays and the answer
cannot tell them apart. That indifference is the point next to 1202: here the
quotient *is* the answer and no representative is ever built.

Union the row and column labels rather than the stones, so the graph has at most
`2n` vertices and takes one union per stone instead of `O(n^2)` pairwise checks.

`O(n alpha(n))`.

## Files

- `python/solution.py`
