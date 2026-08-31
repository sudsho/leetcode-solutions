# 1202. Smallest String With Swaps

Difficulty: Medium
Topics  : Union-find + picking a representative of an orbit

## Problem

Given `s` and a list of index pairs, any pair may be swapped any number of
times. Return the lexicographically smallest reachable string.

## Approach

The reachable set is the orbit of `s` under the group the pairs generate, so the
answer is a representative of one orbit rather than the orbit itself.
Transpositions along a connected graph generate the full symmetric group on its
vertices, so the group is `prod Sym(C)` over the components of the pair graph and
the edges themselves can be discarded once merged - only the partition survives.
Lex order is not equivariant under that group and does not need to be: the
minimum is taken inside a single finite orbit, and the problem supplies the order
rather than the solution having to find one. Sorting each component's characters
into its own positions is a per-component exchange argument, since the characters
available at a position are exactly the unused ones from its component.

`O(n alpha(n) + m + n log n)`.

## Files

- `python/solution.py`
