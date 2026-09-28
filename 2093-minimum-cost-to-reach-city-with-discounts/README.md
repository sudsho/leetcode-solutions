# 2093. Minimum Cost to Reach City With Discounts

Difficulty: Medium
Topics  : Dijkstra with a second coordinate that is monotone, the discounts-left bar as 1928's time bar turned around, why the bar at the push fails badly once the cost sits on the road, and why the once-per-highway rule never binds

## Problem

`n` cities joined by undirected highways `[city1, city2, toll]`. Up to
`discounts` times, a highway may be driven for `toll / 2` (integer division),
at most once per highway. Return the least cost from city 0 to city `n - 1`,
or -1.

## Approach

The state is `(city, discounts left)`, the same shape as 1928's `(city, time)`,
and it does not collapse either: the cheap arrival may have spent the discount
the rest of the route wanted. The difference is that this coordinate is
monotone. A discount left over never costs anything, so a state is dominated
by any state at the same city that is no dearer and has at least as many left.

Two searches follow. The layered one settles each of the `k + 1` copies of a
city once. The Pareto one is 1928's argument turned around: pops come in cost
order, so one number per city, the most discounts any earlier pop still had
there, is the whole frontier, and a pop is expanded only if it beats it.

The once-per-highway rule looks like it needs another coordinate and does not.
Tolls are non-negative, so cutting a cycle out of a walk never raises its toll
and frees whatever discounts it used. Some simple path is optimal, and a simple
path uses each highway once.

## Exhaustive, against a path-enumeration oracle

The oracle keeps no state. It enumerates every simple path from 0 to `n - 1`
and puts the discounts on each path's dearest roads, which is where a
discount saves most since the saving `toll - toll // 2` grows with the toll.

| cities | tolls | discounts | instances | answerable | layered | Pareto | bar at push | one label | discount after |
|---|---|---|---|---|---|---|---|---|---|
| 4 | every graph, {absent, 1, 3, 4} | 0..3 | 16384 | 15816 | 0 | 0 | 12218 (77%) | 254 (1.6%) | 514 (3.3%) |
| 5 | every graph, {absent, 1, 4} | 0..2 | 177147 | 172062 | 0 | 0 | 125466 (73%) | 4923 (2.9%) | 0 |
| 5 | every graph, {absent, 2, 7} | 0..2 | 177147 | 172062 | 0 | 0 | 125466 (73%) | 4875 (2.8%) | 3504 (2.0%) |
| 5 | every graph, {absent, 0, 3} | 0..2 | 177147 | 172062 | 0 | 0 | 75144 (44%) | 0 | 0 |

Random multigraphs, wrong counts:

| n | highways | tolls | k | graphs | answerable | layered | Pareto | bar at push | one label | discount after |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 10 | 0..10 | 1 | 4000 | 3653 | 0 | 0 | 3495 | 669 (18%) | 54 |
| 6 | 10 | 0..10 | 2 | 4000 | 3639 | 0 | 0 | 3470 | 229 | 51 |
| 8 | 16 | 0..100 | 2 | 2000 | 1913 | 0 | 0 | 1904 | 364 (19%) | 89 (4.7%) |
| 10 | 20 | 0..100 | 3 | 1000 | 962 | 0 | 0 | 960 | 86 | 26 |
| 10 | 30 | 0..1000 | 5 | 500 | 498 | 0 | 0 | 498 | 1 | 0 |

## What the columns say

- **The bar at the push is the worst reading by far**, 44% to 77% exhaustively
  and 95% to 100% on random graphs. It has two faults stacked. At `k = 0` it is
  1928's tolled-road failure, the first push into a city is not the cheapest
  one, and that alone is 356 of 3954 answerable four-city graphs, 9%. With
  discounts, the full-price push into a city sets the bar at the discounts it
  still has, and the discounted push, carrying one fewer, can never beat it.
  The search almost never spends a discount.
- **One label per city** is the layered search with the layers merged. The
  smallest failure is two roads, `0-2` at 1 and `2-3` at 3, one discount: city
  2 is reached for 0 by spending it on the cheap road, gets settled, and the
  3 is paid in full. Answer 2, it says 3. Under 3% exhaustively and 18% to 19%
  on the random graphs with few discounts, falling to nothing once there are
  more discounts than any route has roads.
- **Shortest route first, then discount it** fails when a route that loses at
  full price wins after halving. It is never wrong with tolls {1, 4} at five
  cities, which is a coincidence of those two values (one road of 4 halved and
  three roads of 1 with one made free both cost 2), and 2% with {2, 7}.
- **With tolls in {0, 3}** every paid road saves the same amount, so only the
  push bar can go wrong.

## At the statement's size

`n <= 1000`, `highways <= 1000`, tolls to 10^5, `discounts <= 500`. The
frontier is 3.9 to 8.6 states per city on average, with a maximum of 17 out of 501
possible, because a discount beyond the number of roads on the route saves
nothing. That makes the Pareto search 0.010s against the layered search's 1.9s
at n = 1000, k = 500. At k = 5 the two are the same, a few milliseconds.

## What I had wrong

Five predictions written before the run. Two right, one half, two wrong.

- **Right:** layered and Pareto both match the oracle everywhere.
- **Wrong:** the bar at the push wrong on about 5%. 73% on five cities, and 9%
  even with no discounts.
- **Half:** one label wrong on about 20%. 18% to 19% on the random graphs with
  one or two discounts, under 3% exhaustively.
- **Right:** discount after wrong on about 3%. 0% to 4.7%.
- **Wrong:** at most 3 states per city on average at the statement's size. 8.6
  on a random tree plus one edge at k = 500.

## Bounds

`O(k m log(k m))` time and `O(k n)` space for the layered search. The Pareto
search has the same worst case and in practice expands a handful of states per
city, bounded by the length of the routes rather than by k. The oracle is
exponential and only runs on small graphs.

## Files

- `python/solution.py`
