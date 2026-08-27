# 711. Number Of Distinct Islands II

Difficulty: Hard
Topics  : Flood fill + counting orbits of a group action

## Problem

Count the 4-connected islands of `1`s in a grid up to translation, rotation and
reflection.

## Approach

"Same shape" is "same orbit under `Z^2 x| D4`", so the answer is the number of
orbits. A hash set needs a representative rather than the orbit itself, so the
work is building a section of the quotient map, and the two halves of the group
need different mechanisms: translations act freely with infinite orbits, so they
get a normal form (shift the least cell to the origin); `D4` is finite but does
not act freely, so there is no fundamental domain and the orbit gets enumerated
and minimised instead.

`O(mn)` for the flood fill, then `O(8 * s log s)` per island of `s` cells.

## Files

- `python/solution.py`
