# 1928. Minimum Cost to Reach Destination in Time

Difficulty: Hard
Topics  : Dijkstra on one criterion under a budget on another, why a single time bar per city is the whole Pareto frontier, and why that bar may be set at the push only because the fees sit on the cities

## Problem

`n` cities joined by undirected roads `[x, y, time]`, possibly several between
one pair. Every city passed through costs `passingFees[i]`, the first and the
last included. Starting at city 0, return the least cost of reaching city
`n - 1` in at most `maxTime` minutes, or -1.

## Approach

Unlike 3342 the extra coordinate does not collapse. Two arrivals at one city
with different times and costs are not comparable, the cheap one may be too
slow to finish and the fast one may be dear, so the honest state is
`(city, time)` with up to `maxTime + 1` times per city.

Dijkstra ordered by cost does not need all of them. Pops come out in cost
order, so when a state pops at city u every earlier pop at u was no dearer, and
the new one is dominated exactly when it is also no faster. One number per
city, the least time any popped state reached it in, is then the whole
frontier: expand a pop only if it beats that time. The first pop at `n - 1`
is the answer, because it is the cheapest arrival among states that respected
the budget.

The common shortcut sets the bar when a state is pushed, before anyone knows
it is the cheapest. That is still right here, and only because of where the
fee sits. A push into v costs the popped cost plus `passingFees[v]`, popped
costs never fall, so pushes into v arrive in non-decreasing cost and a later
push that is no faster really is dominated. Put a toll on the road instead and
two pushes into v can arrive in either order of cost.

## Exhaustive, against a time-indexed oracle

The oracle settles nothing. `at[t][v]` is the least cost of a walk that is at
v at exactly time t, filled in increasing t since every road takes at least a
minute, and the answer is the minimum over `t <= maxTime`.

| cities | roads | fees | maxTime | instances | answerable | Pareto, bar at pop | bar at push | settle once by cost | settle once by time |
|---|---|---|---|---|---|---|---|---|---|
| 4 | every graph, times in {absent, 1, 2} | 1..3 | 1..6 | 354294 | 275643 | 0 | 0 | 0 | 2754 (1.0%) |
| 5 | every graph, times in {absent, 1, 3} | ends 1, middle 1..2 | 2..8 | 3306744 | 2860896 | 0 | 0 | 9654 (0.34%) | 394758 (13.8%) |

Random multigraphs, wrong counts:

| n | roads | tolls | maxTime | graphs | answerable | Pareto | bar at push | settle by cost | settle by time |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 10 | none | 12 | 4000 | 3632 | 0 | 0 | 8 | 431 |
| 10 | 20 | none | 30 | 2000 | 1917 | 0 | 0 | 3 | 659 |
| 30 | 60 | none | 100 | 300 | 284 | 0 | 0 | 0 | 162 |
| 6 | 10 | 0..10 | 12 | 4000 | 3578 | 0 | 580 | 23 | 983 |
| 10 | 20 | 0..100 | 30 | 2000 | 1893 | 0 | 351 | 7 | 889 |

## What the columns say

- **Settling once by cost never went wrong on four cities.** It fails when
  the cheapest arrival at some city is too slow to finish and a dearer,
  faster one would have. That takes two routes into a middle city and a road
  out of it, and with fees on the cities the cheaper of two routes is usually
  the one through fewer of them, so four cities leave little room. The first
  failure at five is `0-3, 3-1, 1-2` at 1 minute each, `3-2` at 3, `2-4` at 1,
  fees all 1, `maxTime = 4`: the cheap arrival at 2 is at time 4 and the
  answer is 5 the long way round. It is rare because the budget has to bind
  in exactly the right place, 0.34% at five cities and under 0.25% on the
  untolled random graphs.
- **Settling once by time is the common failure**, 1% at four cities, 13.8% at
  five and 12% to 57% on the random graphs, because the fastest arrival is
  often the dearest and the budget is usually loose enough to afford a slower
  one.
- **The bar at the push is never wrong on the problem as stated** and is wrong
  on 16% and 19% of answerable graphs once roads carry tolls. The argument for
  it is the one about where the cost sits, and the counts follow it exactly.

## At the statement's size

`edges <= 1000` and `n - 1 <= edges`, so at n = 1000 the graph is a tree plus
an edge and the frontier is 1.01 states per city, max 2. With 1000 roads on
100 cities it is 5.9 to 6.0 per city with a maximum of 14, and on 30 cities 3.7
with a maximum of 11. Each run returns in under a millisecond and agrees with
the oracle.

## What I had wrong

Five predictions written before the run. One right, two half, two wrong.

- **Right:** the Pareto search matches the oracle everywhere.
- **Wrong:** settling once by cost wrong on about 15%. Never at four cities,
  0.34% at five. I was picturing the budget binding far more often than it does.
- **Half:** settling once by time wrong on about 25%. 1% at four cities, 13.8%
  at five, 12% to 57% on random graphs.
- **Half:** the bar at push wrong on under 2%. Right by the letter, since it is
  never wrong, but I had it down as a rare bug and it is a correct shortcut that
  depends on the fees being on the cities.
- **Wrong:** at most 10 states per city at the statement's size. 14 on 100
  cities with 1000 roads.

## Bounds

`O(T m log(T m))` time and `O(T n)` space in the worst case, T = `maxTime`,
since a city can hold at most T + 1 frontier times. The oracle is `O(T (n + m))`
and at these limits is the same order.

## Files

- `python/solution.py`
