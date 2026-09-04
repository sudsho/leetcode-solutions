# 685. Redundant Connection II

Difficulty: Hard
Topics  : Union-find + in-degree case split, and a tie broken by the input rather than by the structure

## Problem

A rooted tree on `n` nodes with one extra directed edge added, given as `n`
directed edges. Remove one edge so that what remains is a rooted tree. If more
than one edge qualifies, return the one that occurs last in the input.

## Approach

`n` edges over `n` nodes, and a rooted tree wants every in-degree equal to 1
except the root's. That leaves two cases and they are disjoint.

**Exactly one node has two parents.** Call the two edges `first` and `second` by
input position; one of them has to go. Try `second`: union everything else and
check for a cycle. No cycle means `second` is an answer, and it is the later of
the two, so it is the answer regardless of whether `first` also works. A cycle
means `first` is on it and `second` is the only answer.

**No node has two parents.** Every in-degree is 1 and the graph is connected, so
there is exactly one directed cycle and *every* edge on it is a valid answer.
Union in input order and return the first edge that closes a cycle, which is the
last cycle edge scanned and therefore last in input order.

`O(n * alpha(n))` time, `O(n)` space.

The order of the two trials in the first case is not free. If `first` is tried
first it wins whenever both candidates work - and both work whenever the
two-parent node is off the cycle - so the routine would return a legal edge and
the wrong one. The statement's tie-break convention is compiled into that line.

## Why this problem

To break the rule the log has been sharpening since 711: a printed choice off a
class is free exactly when the printed function factors through the quotient.
It was tested on 711, 721, 1061 and 1202, all of which answer the question
structurally. Here the structure declines to, and the tell is syntactic and
sits in the statement: "if there are multiple answers, return the answer that
occurs last in the input". The graph is the same object under any reordering of
`edges`; the answer is not. So the printed function does not factor through the
quotient and no argument is owed anyway, because the tie was legislated instead
of discovered. The "only if" half of the rule does not survive it, and neither
do the four candidate axes before it - all five were hunting for a structural
reason a choice is free, and stipulation is not one.

Three entries running had it that the pairs are a presentation and only the
quotient survives. Here the presentation is the answer.

## Size of the answer set

`all_valid_removals` in the solution file is an `O(n^2)` oracle that removes each
edge and tests the result against the definition. It is not used by the
solution; it is there because the answer is a choice out of a set and the set is
what says how large the choice is. Every account of this problem I have read
describes the ambiguity as two candidates. That holds only in the two-parent
case. On a directed cycle of length `L` all `L` edges are valid, so the answer
set has size 1, 2, or `L`, and `L` runs up to `n`.

Measured by the `__main__` run:

```
[[1, 2], [1, 3], [2, 3]]                   -> [2, 3]    |valid|=2 at [1, 2]
[[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]   -> [4, 1]    |valid|=4 at [0, 1, 2, 3]
[[2, 1], [3, 1], [4, 2], [1, 4]]           -> [2, 1]    |valid|=1 at [0]
[[1, 2], [2, 3], [3, 1]]                   -> [3, 1]    |valid|=3 at [0, 1, 2]
[[4, 2], [1, 4], [3, 1], [1, 3]]           -> [1, 3]    |valid|=2 at [2, 3]
[[3, 1], [2, 3], [1, 2], [1, 4]]           -> [1, 2]    |valid|=3 at [0, 1, 2]
```

The run also asserts that what comes back is the *last* valid index, which is
the part of the specification the fast routine implements without ever
evaluating it.

## Files

- `python/solution.py`
