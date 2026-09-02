# 1061. Lexicographically Smallest Equivalent String

Difficulty: Medium
Topics  : Union-find + a printed function of a class that is not a member of it

## Problem

`s1[i]` is equivalent to `s2[i]` for every `i`, and equivalence is closed under
reflexivity, symmetry and transitivity. Return the lexicographically smallest
string obtainable from `baseStr` by replacing each letter with one equivalent
to it.

## Approach

Union-find over the 26 letters, with the smaller letter always taken as the
parent, so `find` returns the minimum of the class instead of an arbitrary
label and no `root -> min` table is needed between the structure and the
answer. Then map `baseStr` through `find`.

Picked to run the test the 721 entry left open, which was that a printed choice
off a class is free exactly when the printed function factors through the
quotient, checkable before writing anything. `min` is a function of the class,
so it factors, so the choice is free; that holds. The reason it is worth keeping
is that it splits that rule from the paraphrase written beside it - "a choice
needs an argument when the observable part varies across the class" - which
gives the wrong answer here, since the observable part varies as much as it
possibly can and no argument is owed. The paraphrase assumed the printed thing
is a member picked out of the class, and `min` is an aggregate over all of it.

Against 1202, which is the same union-find and the same phrase in the statement:
there the output is a bijection from a class's positions to its characters, so
the characters are a shared resource and the assignment needs an exchange
argument. Here the objective decomposes over positions, each reporting its own
class's minimum with nothing spent, so the pointwise minimiser is the global one.

`O(|s1| * alpha + |baseStr|)` time, `O(1)` space - the structure is 26 cells
wide whatever the input length says.

## Files

- `python/solution.py`
