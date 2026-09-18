# 1786. Number of Restricted Paths From First to Last Node

Difficulty: Medium
Topics  : Dijkstra, counting over a potential rather than over shortest paths, the first pull that needs a filter, and a count that depends on the heap's tie-break

## Problem

A connected undirected graph on nodes `1..n` with positive edge weights. Let
`d(x)` be the shortest distance from `x` to `n`. A restricted path from `1` to
`n` is one where `d` strictly falls at every step. Count them, modulo
`10^9 + 7`.

## Approach

Dijkstra from `n`, then count at the moment each node is settled:

```python
for u in order:
    if u == n:
        ways[u] = 1
    else:
        ways[u] = sum(ways[v] for v, _ in adj[u] if settled[v] and dist[v] < dist[u])
    settled[u] = True
```

A restricted path out of `u` steps to a neighbour strictly closer to `n`, and
every such neighbour is settled before `u` because Dijkstra settles in
nondecreasing distance. So the predecessors are enumerable at the moment they are
needed, which is the 17th's sentence, and there is one line in the loop that the
last five problems did not need, the filter.

## The filter

The oracle enumerates every simple path from 1 to n and keeps the ones whose
distances fall, with distances from Floyd-Warshall rather than from the
Dijkstra. A strictly falling path cannot revisit a node, so the simple paths are
all of them.

| n | weights | connected graphs | with a tied edge | strict | `<=` | none | none, ties broken high |
|---|---|---|---|---|---|---|---|
| 3 | 1..3 | 54 | 9 | 0 | 0 | 0 | 9 |
| 4 | 1..3 | 3834 | 1773 | 0 | 216 | 216 | 1452 |
| 5 | 1..2 | 55248 | 42872 | 0 | 8124 | 8124 | 33960 |

(wrong counts in the last four columns.)

- **strict**: right on all of them, and on 14000 random graphs at n = 9.
- **`<=` and no filter are the same program.** A settled neighbour already has
  `dist[v] <= dist[u]`, asserted equal on every graph, so the only thing the
  filter removes is a neighbour at the same distance.
- **what a tie does**: a neighbour at the same distance that happened to settle
  first gets counted as a step, and a step that does not fall is not a
  restricted step. Every wrong answer is on a graph with an edge between two
  nodes at equal distance, asserted, and on the random graphs every wrong answer
  is too big, 3751 of 3751.

The smallest one is four nodes, `1-3, 2-3, 2-4, 3-4`, all unit weights. 2 and 3
are both one from `n`, 2 settles first, and 3 picks up 2's path along the rung,
so the answer comes out 2 instead of 1.

## The count depends on the tie-break

With no filter, which of two tied nodes counts the other is the heap's choice.
Break ties on the smaller id and node 1 settles first in its distance group, so
it never picks up a neighbour at its own distance, and the only errors come from
ties further down. Asserted: no default-order error on a graph whose every tied
edge touches node 1. Break them on the larger id and node 1 settles last:

- wrong on 216 of 3834 graphs one way and 1452 the other at n = 4, 8124 and
  33960 of 55248 at n = 5
- the two orders give different answers on 1344 and 32160 graphs

So a rate measured for the unfiltered program is a rate for a heap, not for a
graph.

## At the statement's size

Random graphs at `n = 20000, m = 40000` have almost nothing to count. The
answers were 3, 2 and 1, and the modulus never came near. The instance that needs
it is a ladder: pairs of nodes, all four unit edges from one pair to the next, a
tied rung inside each pair, and the last pair joined to `n`. `2^(layers - 1)`
restricted paths with or without the rungs.

```
  layers=   20 rungs=False n=    41 m=    78  answer     524288   exact 6 digits   unfiltered/exact 1   flipped 1
  layers=   20 rungs=True  n=    41 m=    98  answer     524288   exact 6 digits   unfiltered/exact 2217   flipped 4434
  layers= 7999 rungs=False n= 15999 m= 31994  answer  532856372   exact 2408 digits   unfiltered/exact 1   flipped 1
  layers= 7999 rungs=True  n= 15999 m= 39993  answer  532856372   exact 2408 digits   unfiltered/exact ~1e1409   flipped ~1e1409
```

With the rungs, the unfiltered count grows by 3 per pair against 2, which is
1.5^19 = 2217 at 20 layers, and flipping the tie-break doubles it again at the
top, because node 1 then also takes node 2's count. At the full size the
unfiltered count is off by 1409 digits. 0.03s for the solution there.

## What I had wrong

Four predictions written before the run.

- **Right:** the strict pull matches the oracle everywhere. The flip changes the
  unfiltered answer on at least one graph (on 32160 at n = 5). More than 30% of
  the n = 5 graphs have a tied edge, and it is 78%.
- **Wrong:** the unfiltered pull wrong on more than half of the graphs with a
  tie. Under the default order it is 12% at n = 4 and 19% at n = 5. Under the
  flipped one it is 82% and 79%. So the prediction held for one heap and not the
  other, and I had not thought of the heap as a variable.

I put the `<=` filter in expecting it to land between the other two. It cannot,
since a settled neighbour is never further away, and I should have seen that
before writing it.

## Bounds

At least one restricted path, the shortest path from 1 to `n`, since every step
along it falls. Exponential at worst: the ladder has `2^((n - 3) / 2)`, and
layers of three nodes would grow like `3^(n / 3)`, which is more. I have not
worked out the maximum. Dijkstra `O(m log n)`, and the pull reads each adjacency
list once, `O(n + m)`.

## Files

- `python/solution.py`
