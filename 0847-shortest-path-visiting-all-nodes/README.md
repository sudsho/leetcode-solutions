# 847. Shortest Path Visiting All Nodes

Difficulty: Hard
Topics  : BFS on (node, mask) from every node at once, 864's antichain bar on a graph where every node is its own key, the count bar that dies on a path of four, and an order experiment that turns out to be one experiment twice

## Problem

An undirected connected graph on `n` nodes, `n <= 12`. Return the length of
the shortest walk that visits every node, starting anywhere and revisiting
nodes and edges as it likes.

## Approach

The state is `(node, mask of nodes visited)`, with every `(u, {u})` in the
queue at level 0. As in 864 the mask is a partial order: `{0, 1}` and `{0, 2}`
at node 0 are incomparable. So the bar at a node is the set of masks already
queued there with none a subset of another, a push is dropped when a queued
mask contains it, and a surviving push evicts the subsets it dominates. Every
edge costs 1, so the bar goes on at the push. Every mask queued at `u` holds
`u`, so the set is at most `C(n - 1, (n - 1) // 2)` wide, 462 at `n = 12`.

What is different from 864 is that there are no locks. Every node is a key,
the mask grows at every first visit, and nothing is ever walled off.

## Exhaustive, against a layer oracle

Every connected graph on `n` labelled nodes, every edge subset that is
connected. The oracle keeps each layer as a set of states with nothing marked
and agrees with the layered search on every graph to `n = 5` and every seventh
at `n = 6`.

| n | graphs | antichain bar | count bar | count mark | one mark | pops saved | widest | bound |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 0 | 0 | 0 | 4 | 0.0% | 2 | 2 |
| 4 | 38 | 0 | 6 (15.8%) | 6 | 38 | 0.0% | 3 | 3 |
| 5 | 728 | 0 | 215 (29.5%) | 215 | 728 | 0.2% | 6 | 6 |
| 6 | 26704 | 0 | 11246 (42.1%) | 11246 | 26704 | 3.4% | 10 | 10 |

Random connected graphs on 8 nodes, a random tree plus random edges, 2000 at
each edge count. The bound is `C(7, 3) = 35`.

| edges | count bar | count mark | antichain bar | pops saved | widest |
|---|---|---|---|---|---|
| 7 | 83.3% | 83.3% | 0 | 0.0% | 35 |
| 9 | 76.6% | 76.6% | 0 | 9.6% | 28 |
| 12 | 67.1% | 67.1% | 0 | 14.1% | 26 |
| 16 | 41.0% | 41.0% | 0 | 13.3% | 31 |
| 22 | 11.9% | 11.9% | 0 | 5.1% | 35 |
| 28 | 0.0% | 0.0% | 0 | 0.0% | 35 |

## What the columns say

- **The count bar**, one number per node, the most nodes any queued arrival
  had visited, dies on the path `3 - 0 - 1 - 2`. The answer is 3. The arrival
  at 1 holding `{0, 1, 2}` sets the bar at 1 to 3, and the arrival at 0
  holding `{0, 1, 3}`, which needs to go through 1 to reach 2, is then dropped
  at 1 for holding no more. It says -1. On the 728 graphs at `n = 5` it is
  wrong on 215, says -1 on 49 of them and too long on the rest, 7 where the
  answer is 4. The sparser the graph the worse: 83% on trees of 8 nodes and
  0% at 28 edges.
- **The count mark**, one visited mark per `(node, number visited)`, `n^2`
  states for `n 2^n`, is wrong on exactly the same graphs as the count bar.
  Every exhaustive row, every random row, and every order below. It keeps
  strictly more states and it never helps. I do not have the argument.
- **One mark per node is dead before the first pop**, because every node is
  a start and so every node is marked. Wrong on every graph with `n >= 3`,
  for a reason that has nothing to do with order, so 864's open question
  about the move order cannot be asked of it here.
- **It can be asked of the count bar, and the answer comes in two halves.**
  At `n = 5`, all 120 adjacency orders are wrong on exactly 215 graphs and
  all 120 start orders are wrong on exactly 215, and the 215 is a different
  set under every one of the 240. At `n = 6` the count moves with the order,
  11037 to 11246 over six sampled orders. And for each permutation the
  adjacency column and the start column have the same count on different
  sets, which is a relabelling: sorting the adjacency lists of `G` by `pi` is
  the default search on `pi(G)` with the starts in the order `pi` lists them,
  and the set of labelled connected graphs is closed under relabelling. So
  that was one experiment run twice. Why the count is fixed at `n <= 5` and
  not at `n = 6` I do not have.
- **The antichain reaches its bound** at every `n` in the exhaustive table,
  on trees and on dense graphs at 8 nodes, and 462 of 462 at 12 nodes from
  45 edges up.
- **The bar fires in the middle of the edge range and never at the ends.** On
  a tree a mask is a subtree, the cheapest walk covering `S` and ending at `w`
  costs `2 E(S) - max_{s in S} d(s, w)`, and adding `k` nodes to `S` adds
  `2k` edges and at most `k` to that distance, so a superset always arrives
  strictly later and the bar has nothing to drop. On the complete graph
  `(w, M)` is first reached at level `|M| - 1`, same thing. Measured, 0.0%
  of the pops saved on both, and up to 47% at 20 edges on 12 nodes.

## At the statement's size

12 nodes, three random graphs at each edge count.

| edges | layered pops | time | antichain pops | time | saved | widest | count bar wrong |
|---|---|---|---|---|---|---|---|
| 11 | 975 to 2753 | 0.00 to 0.01s | the same | 0.01 to 0.02s | 0% | 23 to 77 | 3 of 3 |
| 14 | 2479 to 4176 | 0.00 to 0.01s | 1792 to 3130 | 0.01 to 0.02s | 21% to 28% | 30 to 62 | 2 of 3 |
| 20 | 8075 to 10201 | 0.01s | 5413 to 5496 | 0.06s | 33% to 47% | 85 to 86 | 2 of 3 |
| 30 | 19584 to 20436 | 0.02 to 0.03s | 14484 to 15562 | 0.6 to 0.8s | 22% to 28% | 292 to 330 | 1 of 3 |
| 45 | 23640 to 24009 | 0.03s | 22485 to 23146 | 2.2 to 2.3s | 4% to 5% | 462 | 0 of 3 |
| 66 | 24433 | 0.04 to 0.06s | 24433 | 3.4 to 3.7s | 0% | 462 | 0 of 3 |

Each push scans the node's antichain in Python, and at 462 masks a node that
is 70x slower than a bit test for a saving of 4%. 864 was 2.1x slower at its
worst. The bar is right everywhere and worth having nowhere on this problem.

## What I had wrong

Seven predictions written before the run. Three right, one half, three wrong.

- **Right:** layered and the antichain bar match the oracle on every connected
  graph to `n = 6`.
- **Wrong:** the count bar wrong on about 10% at `n = 5` and 30% at `n = 6`.
  29.5% and 42.1%.
- **Wrong:** the count mark wrong on about 15% at `n = 5`. 29.5%, and on
  exactly the count bar's graphs.
- **Wrong:** the adjacency order moves the count bar's wrong count by at least
  20% at `n = 5`, the start order by less. Neither moves it at all at
  `n = 5`, and the two are the same experiment.
- **Right:** the widest antichain reaches the bound, 6 at `n = 5` and 10 at
  `n = 6`.
- **Half:** at 12 nodes the bar saves over half the pops on a tree and under
  10% on the complete graph, and is slower everywhere. 0% on a tree, with
  an argument, 0% on the complete graph, and 2x to 70x slower.
- **Right:** the fewest-edges failure of the count bar has 4 nodes. The path
  on 4 nodes.

## Bounds

`O(2^n (n + m))` time and `O(n 2^n)` space for the layered search. The
antichain bar holds at most `C(n - 1, (n - 1) // 2)` masks per node and scans
them on each push, so its worst case is `O(2^n (n + m) C(n - 1, (n - 1) // 2))`,
and the oracle is `O((n 2^n)^2)`.

## Files

- `python/solution.py`
