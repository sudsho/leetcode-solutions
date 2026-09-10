# 1976. Number of Ways to Arrive at Destination

Difficulty: Medium
Topics  : Dijkstra with path counting, and a complexity-only guard that is only complexity-only next to the right neighbour

## Problem

`n` intersections, undirected roads `[u, v, time]` with `time >= 1`, every
intersection reachable. Return the number of shortest-time routes from `0` to
`n - 1`, modulo `10^9 + 7`.

## Approach

Dijkstra, carrying `ways[v]` beside `dist[v]`. A strict improvement resets
`ways[v]` to `ways[u]`; an equal offer adds `ways[u]` to it. Every weight is at
least 1, so a predecessor on a shortest path is strictly closer and has been
popped - with its count final - before anything it feeds.

## The line

```python
d, u = heapq.heappop(heap)
if d > dist[u]:
    continue
for v, w in adjacent[u]:
    candidate = d + w        # or dist[u] + w
```

With the guard in place `d == dist[u]` on every pop that reaches the loop, so
what the relaxation reads is a free choice. Four programs, then:

| guard | reads     | every graph on 4 nodes, w <= 3 | every graph on 5 nodes, w <= 2 |
|-------|-----------|--------------------------------|--------------------------------|
| yes   | `d`       | 0 wrong of 3954                | 0 wrong of 57354               |
| yes   | `dist[u]` | 0 wrong                        | 0 wrong                        |
| no    | `d`       | 0 wrong                        | 0 wrong                        |
| no    | `dist[u]` | **18 wrong**                   | **90 wrong**                   |

Against a Floyd-Warshall oracle that counts over the tight-edge DAG and has no
heap in it.

**Without the guard, reading `d`.** A stale pop has `d > dist[u]`, and `u`'s
real pop already relaxed every neighbour, so `dist[v] <= dist[u] + w < d + w`.
Neither branch fires. Harmless, and it costs:

```
  n=  10  guarded=     90   unguarded=      414   ratio=   4.6   dist[u] version says 10404
  n=  50  guarded=   2450   unguarded=    60074   ratio=  24.5   dist[u] version says 815547185
  n= 100  guarded=   9900   unguarded=   490149   ratio=  49.5   dist[u] version says 551366525
  n= 200  guarded=  39800   unguarded=  3960299   ratio=  99.5   dist[u] version says 801604727
```

That is the staircase, a complete graph with `w(i, j) = 2(j - i) - 1`: the true
distances run along the unit chain and each pop offers every later node a
strictly better tentative, so node `j` carries `j - 1` stale entries. Scans are
exactly `n(n-1)` against `(n-1)(1 + n(n-1)/2)`, asserted as identities. The true
answer is 1 at every size.

**Without the guard, reading `dist[u]`.** Now a stale pop offers
`dist[u] + w`, which equals `dist[v]` on every tight edge out of `u` - not by
coincidence, by the definition of tight. Each one adds `ways[u]` again.

## Why this problem

1163 and 1345 each turned up a line that no part of the correctness argument
mentions and that is the entire complexity bound, and the 9th measured that how
easily such a line hides from testing is a per-instance fact. Both nights
treated the property as belonging to the line. The Dijkstra stale-entry skip is
the textbook member of the class, and counting is the variant where it has a
neighbour: a choice the guard makes invisible, and that decides whether the
guard is load-bearing for the answer.

It does. The same deletion is an `n/2`-fold slowdown in one program and a wrong
answer in another, and the two programs are textually identical wherever the
guard is present.

## What I had wrong

I predicted the `dist[u]` version would be wrong mostly at small weight ranges,
where different paths tie often, and would hide at large ones.

```
  w in [1,     1]  stale pops in   0/400   dist[u] version wrong on   0/400   unguarded scan ratio 1.00x
  w in [1,     2]  stale pops in 399/400   dist[u] version wrong on  56/400   unguarded scan ratio 1.17x
  w in [1,     3]  stale pops in 400/400   dist[u] version wrong on  69/400   unguarded scan ratio 1.32x
  w in [1,     5]  stale pops in 400/400   dist[u] version wrong on 112/400   unguarded scan ratio 1.52x
  w in [1,    10]  stale pops in 400/400   dist[u] version wrong on 127/400   unguarded scan ratio 1.76x
  w in [1,   100]  stale pops in 400/400   dist[u] version wrong on 176/400   unguarded scan ratio 2.10x
  w in [1, 10000]  stale pops in 400/400   dist[u] version wrong on 164/400   unguarded scan ratio 2.15x
```

Random graphs, `n = 40`, edge probability 0.3. The error rate rises with the
weight range and does not come back down, because the equality it trips is the
tight edge itself and there is one of those on every shortest path whatever the
weights are. The only range where it is invisible is `w = 1`, and for a
different reason than the one I had: with every weight equal the pops come out
in BFS order, no node is improved after it is first pushed, and there are no
stale entries at all. The bug is not rare there, it is absent.

The small exhaustive sets are the other half of it. 90 wrong of 57354 is 0.16%,
and 18 of 3954 is 0.46% - the kind of graph a person writes by hand to test
Dijkstra is exactly where this version is almost always right.

## Bounds

The answer is at least 1, since every intersection is reachable. It is not
polynomially bounded: `n - 2` middle nodes in layers of three, all weights 1,
consecutive layers fully joined, give `3^((n-2)/3)` shortest routes, which is
`3^66` at `n = 200`, and that is why the modulus is there. Guarded, each node is
popped for real once and scans its adjacency once, `O((n + E) log n)`. Unguarded
and reading `d`, every push is a strict improvement along a directed edge, so a
node carries at most its degree in entries and the scan is at most
`sum deg(u)^2`, which is `O(n^3)` on a complete graph and which the staircase
attains to within a factor of two.

## Files

- `python/solution.py`
