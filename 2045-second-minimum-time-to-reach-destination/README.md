# 2045. Second Minimum Time to Reach Destination

Difficulty: Hard
Topics  : BFS with two slots per vertex, the settle argument asked for a second value instead of a first, and three ways of reading "second" that are each wrong on a different share of graphs

## Problem

An undirected connected graph on vertices 1..n. Every edge takes `time`
minutes. Every vertex has a signal that is green on `[0, change)`, red on
`[change, 2 change)`, and so on, all in phase. A walker may arrive at any time,
may leave only on green, and may not wait on green. Revisiting vertices and
edges is allowed. Return the second smallest time, strictly larger than the
smallest, at which vertex n can be reached from vertex 1.

## Approach

Every edge costs the same and every signal is in phase, so the arrival time
after k edges is a function of k alone, and a strictly increasing one:

```python
t = 0
for _ in range(k):
    t = leave(t, change) + time
```

So the question is the second smallest walk length from 1 to n, strictly larger
than the smallest. A BFS that keeps two slots per vertex, the smallest and the
second smallest distinct count, and queues a vertex again when its second slot
is written:

```python
if nd < d1[v]:
    d1[v] = nd; queue.append((v, nd))
elif d1[v] < nd < d2[v]:
    d2[v] = nd; queue.append((v, nd))
```

The last four nights put the settle argument on one condition, that the update
cannot improve a value. This asks it for something it was never asked for: not
the first value to be final when it pops, but the second. BFS pops in order of
count, so the second distinct count to reach a vertex is final for the same
reason the first is, and each vertex is queued at most twice.

The second count is always `d1 + 1` or `d1 + 2`, since walking to the last
vertex before n, back and forward again adds two.

## Exhaustive, against the layer oracle

The oracle keeps no distances. Layer 0 is `{1}`, layer L+1 is the neighbour set
of layer L, and the answer is the second L whose layer contains n. The clock
column runs the same two-slot search on clock times with the signal rule at
every step, under four `(time, change)` pairs, and compares with `travel(d2)`.

| n | connected graphs | two-slot wrong | clock wrong | non-strict wrong | first-only wrong (none) | simple paths only wrong (none) | d2 = d1+1 | non-bipartite | non-bipartite at d1+2 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 1 | 0 | 0 | 0 | 1 (1) | 1 (1) | 0 | 0 | 0 |
| 3 | 4 | 0 | 0 | 0 | 2 (2) | 3 (3) | 1 | 1 | 0 |
| 4 | 38 | 0 | 0 | 2 | 14 (14) | 19 (19) | 17 | 19 | 2 |
| 5 | 728 | 0 | 0 | 86 | 217 (208) | 209 (203) | 450 | 533 | 83 |
| 6 | 26704 | 0 | 0 | 4896 | 6512 (5968) | 3841 (3469) | 19921 | 23673 | 3752 |

On random connected graphs the two-slot BFS and the clock search agree with the
oracle on 3000 at n = 10, 1000 at n = 30 and 200 at n = 200, with `time` and
`change` drawn from 1..1000.

## Three readings of "second"

Each of these is a natural first attempt and each fails on its own share.

- **Second route, not second value.** Drop `d1[v] < nd` and a second route of
  the same length fills the second slot. Wrong on 4896 of 26704 at n = 6, 18%,
  every one of them a graph with two shortest routes into n. It returns the
  minimum. The two sets are the same 4896 graphs, checked by counting shortest
  routes separately.
- **Settle once, read the second off the target's neighbours.** An ordinary
  BFS, then the smallest `d1[u] + 1` over neighbours u of n that is larger than
  `d1[n]`. Only first values ever travel, so a second count that has to pass
  through another vertex's second value is invisible. Wrong on 6512 at n = 6,
  24%, and on 5968 of those it finds nothing at all, because every neighbour of
  n is one layer closer. The smallest case is a triangle at the start and one
  edge out: `1-2, 2-3, 1-3, 3-4`. The answer is `1-2-3-4`, three edges, and 4's
  only neighbour is at count 1.
- **Simple paths only.** The statement allows revisits, and the bounce
  `... -> u -> n -> u -> n` is how every bipartite graph gets its `d1 + 2`.
  Wrong on 3841 at n = 6, 14%, and on 3469 of those there is no second simple
  length at all.

All three are only ever too big or missing, never too small, which the run
asserts.

## When the second count is d1 + 1

Parity says a bipartite graph cannot have a walk of length `d1 + 1`, so every
bipartite graph answers `d1 + 2`. The converse fails: 3752 of the 23673
non-bipartite graphs at n = 6 still answer `d1 + 2`, 16%, because their odd
cycle is too far off the shortest routes to cost only one extra edge. On
random sparse graphs at n = 10 it is 923 of 3000.

What decides it exactly is one edge. `d2 = d1 + 1` if and only if some edge
`(u, v)` has `d(1, u) + d(v, n) = d(1, n)`. Along a walk of length `d1 + 1`,
`i + d(w_i, n)` starts at `d1`, ends at `d1 + 1` and changes by 0, 1 or 2 per
step, so one step changes it by exactly 1, and that step is the edge. The test
agrees with the oracle on every graph enumerated.

## At the statement's size

n = 10^4 with `time = change = 1000`: a random graph with 2 x 10^4 edges in
0.03s, answer 13000. A path of 10^4 vertices in 0.01s, answer 20001000, which is
`d1 + 2` edges with a red wait at every other vertex. The same path with a
triangle at vertex 1 answers 19997000, one edge shorter and one edge longer.

## What I had wrong

Five predictions written before the run. Two right, three wrong.

- **Right:** the two-slot BFS matches the layer oracle everywhere, and the clock
  search agrees with `travel` of its count.
- **Wrong:** the non-strict version wrong on about 40% at n = 6. It is 18%. I
  was counting graphs with any second route into n, and only a second shortest
  one fills the slot.
- **Wrong:** settle-once rarely wrong, under 5%. It is 24%, the worst of the
  three, because "every neighbour of n is one layer closer" is common in small
  graphs.
- **Wrong:** simple paths only wrong on about half. It is 14%. Most graphs at
  n = 6 have a second simple length without needing the bounce.
- **Right:** non-bipartite graphs that still answer `d1 + 2`, under a fifth.
  16%.

## Bounds

`O(n + m)` time and `O(n + m)` space: each vertex is queued at most twice and
each queueing scans its adjacency once. `travel` is `O(d2)`, at most `n + 1`
steps.

## Files

- `python/solution.py`
