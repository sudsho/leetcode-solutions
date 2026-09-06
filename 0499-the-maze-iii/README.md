# 499. The Maze III

Difficulty: Hard
Topics  : Dijkstra over resting cells, and a stipulated tie-break promoted into the optimisation key

## Problem

A ball on a grid of empty cells and walls rolls until something stops it. It
falls into the hole if it passes over it mid-roll. Return the instruction string
(`u`, `d`, `l`, `r`) that reaches the hole in the fewest cells travelled; if
several do, return the lexicographically smallest of them, and `"impossible"` if
none does.

## Approach

The ball only ever comes to rest against a wall, so the states are resting cells
and the edges are rolls. Distance is cells travelled, not moves made, so the
weights differ per edge and this is Dijkstra rather than BFS.

The tie-break goes into the key. Each heap entry is `(distance, instructions,
cell)` compared under the lexicographic product order, so the first pop of the
hole is optimal on distance and, among those, least on instructions. A roll that
travels zero cells is discarded rather than pushed.

`O(R * C * log(R * C) * L)` time with `L` the winning string's length, since the
strings are compared and copied rather than pointed at. `O(R * C * L)` space.

## Why this problem

685 two nights ago killed the rule the week had been sharpening - a printed
choice off a class is free exactly when the printed function factors through the
quotient - by producing a tie the statement legislated instead of leaving to be
discovered. The conclusion recorded then was that stipulation is a non-structural
reason a choice is free, and that all five candidate axes had been searching
inside the structure for something sitting outside it.

The question that entry did not ask is what a stipulation *costs*. On 685 it
cost one line: try `second` before `first`. Load-bearing, but free - the case
analysis would have been written the same way regardless, and no part of the
correctness argument mentions the convention. Here it is not free, and the
reason is the finding.

## The monotonicity the key needs, and where it comes from

Dijkstra wants its key monotone under extension: if `a < b` then `a + s < b + s`
for every continuation `s`. Lex order on strings does not have that property.
With `a = "l"`, `b = "lu"`, `s = "d"`: `a < b` but `"ld" > "lud"`. It fails on
exactly the pairs where one string is a proper prefix of the other.

Those pairs cannot arise here, and the reason is supplied by the other component
of the key. Two instruction strings are compared only when their distances are
equal and their endpoints agree. If one were a proper prefix of the other, the
longer would be the shorter plus a nonempty closed walk from that endpoint back
to itself, and every roll that moves at all costs at least one cell - so the
longer string has strictly greater distance. Equal distance rules the prefix
case out.

So the stipulated tie-break is admissible as an optimisation key only because
the thing it is tie-breaking forbids the case where it would misbehave. The two
components of the key are not independent: the primary one licenses the
secondary one. That is a different relationship from 685's, where the
stipulation and the algorithm met at one line and had nothing to say to each
other.

Which splits a word the log had been using as one thing. 685's tie-break was
stipulated and free. This one is stipulated and owes a compatibility proof. What
separates them is not where the choice comes from - both come from the statement
- but whether the choice has to be carried through a construction. A tie-break
carried through an optimisation has to commute with it.

The `moved == 0` guard in the loop is the same fact showing up as code. A roll
into a wall would let a path collect letters without spending distance, which is
precisely the prefix case, so the guard is not only skipping a no-op.

## Size of the tie

`all_optimal_paths` in the solution file is a two-pass oracle - Dijkstra for the
optimal distance, then a depth-first enumeration capped at it - returning every
instruction string that reaches the hole in that distance. It is not used by the
solution; it is there for the same reason 685's was, because the answer is a
choice out of a set and only the set says how large the choice is.

Measured by the `__main__` run:

```
ball=[4, 3]   hole=[0, 1]   -> lul          |optimal|=2 ['lul', 'ul']
ball=[4, 3]   hole=[3, 0]   -> impossible   |optimal|=0 []
ball=[0, 4]   hole=[3, 5]   -> dldr         |optimal|=2 ['dldr', 'rdld']
```

The first case is worth keeping for a reason beyond the tie being nonempty. The
two optimal strings have different lengths and the answer is the longer one:
three moves covering the same six cells as two. Fewest cells and fewest moves are
different objectives, and only one of them is the problem's. The run asserts
that, so a solution that quietly optimised move count would fail rather than
merely disagree.

## Files

- `python/solution.py`
