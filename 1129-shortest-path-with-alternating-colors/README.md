# 1129. Shortest Path with Alternating Colors

Difficulty: Medium
Topics  : BFS on (node, arriving colour), a second coordinate with no order at all, the one place it has one, and 847's relabelling argument in two colours

## Problem

A directed graph on `n` nodes, `n <= 100`, with red edges and blue edges,
self-loops and parallel edges allowed. Return for each node the length of the
shortest path from 0 whose edge colours alternate, or -1.

## Approach

The state is `(node, colour of the edge that arrived)`, with `(0, red)` and
`(0, blue)` both at level 0 so the first edge can be either colour. A state
arrived by `c` leaves by `1 - c`. Every edge costs 1 and the mark goes on at
the push.

847's mask was partly ordered and 2093's discount count was totally ordered.
Here the coordinate has two values and in general neither can stand in for the
other: an arrival by red can only leave by blue, and the blue edges out of `w`
and the red ones go to different places. So the bar is two marks per node and
nothing smaller.

The one exception is a node whose out-edges are all one colour. An arrival
there by that colour can only leave by the other, which the node does not
have, so it answers `w` and goes nowhere. The search records the answer for
such a state and does not queue it. At those nodes there is one live state,
and that is the only sense in which the colour is ordered on this problem: the
arrival that can still move dominates the one that cannot.

## Exhaustive, against a layer oracle

Every pair of red and blue edge sets on `n` labelled nodes, self-loops in, one
edge per `(u, v, colour)`. The oracle keeps every layer as a set of states with
nothing marked, for `2n` layers. Layered and pruned agree with it on all of
them.

| n | instances | one mark, red start first | blue start first | wrong on both | mono mark |
|---|---|---|---|---|---|
| 2 | 256 | 0 | 0 | 0 | 0 |
| 3 | 262144 | 16384 (6.25%) | 16384 (6.25%) | 8192 | 2048 (0.78%) |

Random instances, 5000 at each edge count. The pruned search's saving is in
pops.

| n | edges | one mark | mono mark | pruned saves |
|---|---|---|---|---|
| 6 | 6 | 1.68% | 0.50% | 61.1% |
| 6 | 12 | 16.52% | 3.56% | 34.9% |
| 6 | 24 | 30.50% | 2.78% | 8.1% |
| 6 | 36 | 8.88% | 0.12% | 1.3% |
| 10 | 10 | 2.06% | 0.52% | 60.9% |
| 10 | 20 | 22.26% | 6.42% | 36.2% |
| 10 | 40 | 59.42% | 9.18% | 10.5% |
| 10 | 100 | 2.90% | 0.00% | 0.1% |

## What the columns say

- **One mark per node** keeps whichever colour arrives first. Its fewest-edges
  failure is red `0 -> 1`, red `1 -> 2`, blue `0 -> 1`, answer `[0, 1, 2]`.
  With the blue start first, `(0, blue)` leaves by red, marks 1 as arrived by
  red, and the blue arrival at 1, the only one that can take red `1 -> 2`, is
  dropped. It says -1. With the red start first it is right on this graph.
- **The order question from 864 and 847 has the answer 847 gave.** Red first
  and blue first are each wrong on exactly 16384 of the 262144, on different
  sets that share 8192. Swapping the colours of `G` turns the red-first search
  on `G` into the blue-first search on the swapped graph, and the instances
  are closed under the swap, so the counts have to agree. One experiment run
  twice again, this time on purpose.
- **At `n = 3` every failure says -1**, half where the answer is 2 and half
  where it is 3. A wrong length starts at `n = 4`: red `3 -> 2, 2 -> 3,
  1 -> 3, 0 -> 3` and blue `0 -> 3, 3 -> 1, 3 -> 2, 2 -> 1` is answered
  `[0, 3, 2, 1]` for `[0, 2, 2, 1]`. Over 36000 random instances on 4, 6 and 10 nodes it said -1
  on 9031 nodes, too long on 1001 and too short on none.
- **The mono mark**, one mark at the one-colour nodes and nothing pruned, is
  the pruned search's bar without the pruning. It keeps whichever arrival
  comes first and is wrong whenever the dead one does, 0.78% at `n = 3` and up
  to 9.18% at 10 nodes and 40 edges.
- **Both wrong counts at `n = 3` are powers of two**, `2^18 / 16` and
  `2^18 / 128`. I do not have the argument.
- **The pruning pays where the graph is sparse**, 61% of the pops at one edge
  a node, because most nodes then have one colour out or none. By `n^2` edges
  every node has both and it saves 0.1%.

## At the statement's size

100 nodes, 400 edges, 2000 random instances. Layered 0.107 ms each, pruned
0.103 ms. The test that skips a dead state costs about what popping it would.

## What I had wrong

Seven predictions written before the run. Four right, one half, two wrong.

- **Right:** layered and pruned match the oracle everywhere.
- **Wrong:** one mark per node wrong on about 20% at `n = 3`. 6.25%, though
  59% at 10 nodes and 40 edges.
- **Wrong:** the mono mark wrong on about 5% at `n = 3`. 0.78%.
- **Right:** red first and blue first wrong on the same number at `n = 3`, on
  different sets. 16384 each, 8192 shared.
- **Half:** the pruned search saves about 25% of the pops at `n = 10`. It
  depends on the density, 61% to 0.1%, and 36% at two edges a node.
- **Right:** the fewest-edges failure of one mark has 3 edges.
- **Right:** pruned is no slower than layered at 100 nodes. 0.103 against
  0.107 ms.

## Bounds

`O(n + m)` time and `O(n + m)` space for both searches, two states per node
and every edge read once from the state that leaves by its colour. The oracle
is `O(n (n + m))`.

## Files

- `python/solution.py`
