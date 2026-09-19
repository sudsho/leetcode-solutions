# 3123. Find Edges in Shortest Paths

Difficulty: Hard
Topics  : Dijkstra, the shortest-path DAG read backwards from the target, an equality filter where 1786 had a strict one, and a parent pointer whose error does not depend on the heap

## Problem

An undirected graph on nodes `0..n-1` with positive edge weights, not
necessarily connected. For each edge, say whether it lies on at least one
shortest path from `0` to `n - 1`. If `n - 1` cannot be reached, every answer is
false.

## Approach

One Dijkstra from `0`, then a walk back from `n - 1` over tight edges:

```python
stack = [n - 1]
while stack:
    v = stack.pop()
    for u, w, i in adj[v]:
        if d0[u] + w == d0[v]:
            out[i] = True
            if not seen[u]:
                seen[u] = True
                stack.append(u)
```

The predecessors of `v` on a shortest path from `0` are exactly the neighbours
with `d0[u] + w == d0[v]`. Starting from `n - 1` and only ever moving to a
predecessor means a tight edge off to the side, into a node that does not lead
on to `n - 1`, is never reached. The usual form runs Dijkstra from both ends and
keeps an edge when `d0[u] + w + dn[v]` equals the shortest distance. It is kept
in the file as a second check and agrees on everything below.

## Four ways to get it wrong

The oracle enumerates every simple path from `0` to `n - 1` and marks the edges
of the cheapest ones. No Dijkstra and no distance array. With positive weights a
shortest walk is a simple path, so nothing is missed.

| n | weights | graphs | more than one shortest path | walk tight | 1786's filter | every tight edge | parent chain | parent, ties high |
|---|---|---|---|---|---|---|---|---|
| 3 | 1..3 | 64 | 3 | 0 | 6 | 41 | 3 | 3 |
| 4 | 1..3 | 4096 | 478 | 0 | 966 | 3699 | 478 | 478 |
| 5 | 1..2 | 59049 | 10686 | 0 | 11487 | 55921 | 10686 | 10686 |

(wrong answers in the last five columns. every simple graph, connected or not.)

- **1786's filter** walks back over every neighbour strictly closer to `0`. That
  is a superset of the tight ones, and it is too big every time it is wrong,
  11487 of 11487 at n = 5. With unit weights it is never wrong, 0 of 2000 random
  graphs at n = 10, because a neighbour one step closer is one unit closer and
  that is tight. So the filter that was exactly right for 1786 is right here
  only when the weights cannot tell it apart from the right one.
- **every tight edge**, not walked from `n - 1`: wrong on 95% of the n = 5 graphs,
  always too big. Almost every graph has a tight edge into a node that is not on
  the way to `n - 1`.
- **the parent chain**: the one path the heap recorded. It is only ever too
  small, so it is wrong on exactly the graphs with more than one shortest path,
  which is also how that column was counted. Flipping the tie-break changes
  which edges it marks on 40 graphs at n = 4 and 2466 at n = 5 and changes the
  number it gets wrong on none of them.

That last one is the difference from 1786. There the unfiltered count was wrong
on 8124 graphs one way and 33960 the other, so its failure rate was a rate for a
heap. Here the heap picks which of the tied paths survives and never whether one
of them is lost.

## Random graphs, n = 10

1000 each, `m` edges placed at random, weights in `1..top`.

| m | top | more than one shortest path | 1786's filter wrong | every tight wrong | parent wrong |
|---|---|---|---|---|---|
| 12 | 1 | 169 | 0 | 898 | 169 |
| 12 | 5 | 78 | 315 | 898 | 78 |
| 25 | 1 | 411 | 0 | 999 | 411 |
| 25 | 5 | 232 | 679 | 999 | 232 |
| 25 | 100 | 14 | 763 | 1000 | 14 |

Wider weights make ties rarer and 1786's filter worse, because the gap between
closer and tight opens up.

## At the statement's size

`n = 50000, m = 50000` with random edges mostly leaves `n - 1` cut off from `0`,
so the answer is all false, and 26 edges are marked in the one unit-weight run
that connects them. A 158 x 158 grid of unit edges is the other end: every
monotone lattice path is shortest, all 49612 edges are marked, and the parent
chain marks 314 of them. 0.06 to 0.11s for the solution on all four.

## What I had wrong

Five predictions written before the run.

- **Right:** the tight walk matches the oracle everywhere. Every tight edge is
  wrong on more than 20% at n = 5, and only ever too big. The parent chain is
  only ever too small, and the flip changes its edges on some graph and its
  error count on none. Under a second at the statement's size.
- **Wrong:** 1786's filter wrong on more than half the reachable graphs at
  n = 5. It is 20%, and 0% with unit weights, which I should have seen from the
  weights before running it.

## Bounds

`O(m log n)` for the Dijkstra and `O(n + m)` for the walk back, each adjacency
list read once. The two-sided form costs a second Dijkstra and no walk.

## Files

- `python/solution.py`
