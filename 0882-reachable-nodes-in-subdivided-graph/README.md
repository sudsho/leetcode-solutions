# 882. Reachable Nodes In Subdivided Graph

Difficulty: Hard
Topics  : Dijkstra, and 1976's stale-entry skip feeding two updates that are not a relaxation

## Problem

An undirected graph on `n` nodes where each edge `[u, v, cnt]` is subdivided into
a chain of `cnt` new nodes. Return how many nodes of the new graph are within
`maxMoves` edges of node `0`.

## Approach

Dijkstra on the original graph with edge weight `cnt + 1`, pushing only what is
in budget. Every original node that gets popped is reachable. From an endpoint
`u` the remaining budget walks `min(cnt, maxMoves - dist[u])` nodes into an edge,
and the edge contributes `min(cnt, used[u, v] + used[v, u])` - the two walks can
meet in the middle, and the min is where the overlap is charged.

## The line

```python
d, u = heapq.heappop(heap)
if d > dist[u]:
    continue
answer += 1                              # or count dist <= maxMoves at the end
for v, cnt in adjacent[u]:
    used[u, v] = min(cnt, maxMoves - d)  # or dist[u]; or max(used[u, v], ...)
```

With the guard every node reaches the loop once, with `d == dist[u]`, so the
three choices under it are free and all eight guarded programs are the same
function. Without it, against a BFS on the subdivided graph:

| read      | edge update | count   | 4 nodes, cnt <= 2, budget <= 8 | 5 nodes, cnt <= 1, budget 2-4 |
|-----------|-------------|---------|--------------------------------|-------------------------------|
| `d`       | overwrite   | per pop | **2799 wrong**                 | **6930 wrong**                |
| `d`       | overwrite   | at end  | **120 wrong**                  | **324 wrong**                 |
| `d`       | max         | per pop | **2916 wrong**                 | **7218 wrong**                |
| `d`       | max         | at end  | 0                              | 0                             |
| `dist[u]` | overwrite   | per pop | **2916 wrong**                 | **7218 wrong**                |
| `dist[u]` | overwrite   | at end  | 0                              | 0                             |
| `dist[u]` | max         | per pop | **2916 wrong**                 | **7218 wrong**                |
| `dist[u]` | max         | at end  | 0                              | 0                             |

Of 36864 and 177147 instances, 2916 and 7218 have a stale pop in budget. The
first row is the textbook program.

**The counter** reads nothing, so it is wrong on every instance with a stale pop.

**The overwrite from `d`.** A stale entry's key is strictly larger than the real
one, so it pops second and writes a shorter reach over the right one. The lasso
isolates it - `0 - 2` directly at weight `L`, `0 - 1 - 2` at weight 2, and a long
pendant off node 2:

```
  length=  3  maxMoves=  8  truth=  11  stale pops=1   overwrite from d   -1   from dist[u] +0   counter +1   textbook, both   +0
  length=  5  maxMoves= 10  truth=  15  stale pops=1   overwrite from d   -3   from dist[u] +0   counter +1   textbook, both   -2
  length= 10  maxMoves= 15  truth=  25  stale pops=1   overwrite from d   -8   from dist[u] +0   counter +1   textbook, both   -7
  length= 50  maxMoves= 55  truth= 105  stale pops=1   overwrite from d  -48   from dist[u] +0   counter +1   textbook, both  -47
```

**The overwrite from `dist[u]`** writes the value that is already there. **The
max** keeps the larger of the two, whichever is read.

## Why this problem

1976 found that deleting the stale skip is harmless if the relaxation reads `d`
and a wrong answer if it reads `dist[u]`, and I filed the property under the
guard plus the read it hides. That predicts something about any Dijkstra whose
pop feeds more than the relaxation: read `d` and the guard can go. The textbook
solution to this problem reads `d`, and its pop feeds an overwrite and a counter.

The guard cannot go, and the read 1976 condemned is the harmless one. So the
property is not the read either. It is per update, and it is whether the update
absorbs a repeat under the value the read supplies:

| update the stale pop reaches | reading `d`                     | reading `dist[u]`             |
|------------------------------|---------------------------------|-------------------------------|
| strict `<` relaxation        | strictly worse offer, absorbed  | equal offer, absorbed         |
| `==` then `+=` (1976)        | never reached                   | reached, not absorbed         |
| overwrite (882)              | worse value written             | same value written, absorbed  |
| max (882)                    | absorbed                        | absorbed                      |
| counter (882)                | not absorbed                    | not absorbed                  |

That table is fitted to the two problems it was written from, the night it was
written, which is how the last several of these died. It goes in as a table.

## What I had wrong

Before the run I had the overwrite from `d` wrong rarely, on the reasoning that
`min(cnt, used[u, v] + used[v, u])` saturates on most edges and hides a lowered
reach, and wrong less often as the budget grows. The exhaustive sets agree, 120
of 2916 and 324 of 7218. Random graphs do not:

```
  maxMoves=   2  stale pops in   0/300   counter wrong   0   overwrite-from-d wrong   0   textbook minus guard wrong   0
  maxMoves=   5  stale pops in  55/300   counter wrong  55   overwrite-from-d wrong  55   textbook minus guard wrong  55
  maxMoves=  10  stale pops in 279/300   counter wrong 279   overwrite-from-d wrong 278   textbook minus guard wrong 278
  maxMoves=  20  stale pops in 300/300   counter wrong 300   overwrite-from-d wrong  54   textbook minus guard wrong 298
  maxMoves=  40  stale pops in 300/300   counter wrong 300   overwrite-from-d wrong   0   textbook minus guard wrong 300
  maxMoves=  80  stale pops in 300/300   counter wrong 300   overwrite-from-d wrong   0   textbook minus guard wrong 300
  maxMoves= 200  stale pops in 299/300   counter wrong 299   overwrite-from-d wrong   0   textbook minus guard wrong 299
```

`n = 30`, edge probability 0.25, `cnt` up to 10. Wrong on 278 of the 279 graphs
with a stale pop at budget 10. It does fall with the budget, but as a cliff and
not a slope: once the budget covers `cnt` from one end or the other, the min
hides the lowered reach, and with `cnt <= 10` that reaches every edge somewhere
between 20 and 40. The small graphs only looked safe because at counts up to 2
almost every edge is saturated before anything goes stale - 1976's 0.16% again,
the instances small enough to enumerate being the ones the bug hides in.

The thing I had no prediction for is that the two bugs cancel. Minus its guard
the textbook program is right on 117 and 288 instances that have a stale pop,
and in every one of them the overwrite undercounts by exactly the number of stale
pops the counter adds back - asserted per instance, not inferred from the table.
The lasso at length 3 is one of them: both bugs present, answer exactly right.

## Bounds

At least 1, node 0 itself, and at most `n + sum(cnt)`. Guarded, each node is
popped for real once and the whole thing is `O(E log E)`. Unguarded, a real pop
pushes each neighbour at most once and a stale pop pushes nothing under either
read - its offer is at least `dist[u] + w`, which cannot beat `dist[v]` - so there
are at most `2E + 1` pushes, and the counter's error is at most `2E`. The
overwrite's error at one end of an edge is the gap between the last stale key at
`u` and `dist[u]`, capped by `cnt`, and the lasso attains `L - 2` of it with a
single stale pop.

## Files

- `python/solution.py`
