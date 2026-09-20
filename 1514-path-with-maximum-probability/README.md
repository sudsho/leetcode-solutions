# 1514. Path with Maximum Probability

Difficulty: Medium
Topics  : Dijkstra where the relation is a product and not a sum, a tie-break that cannot matter because the answer is a scalar, and two ways a float gives up that are not rounding

## Problem

An undirected graph on nodes `0..n-1`. Edge `i` succeeds with probability
`succProb[i]`, all independent. Return the largest probability of getting from
`start_node` to `end_node` along some path, or `0` if there is none.

## Approach

Dijkstra with the heap ordered the other way up, largest product first:

```python
p = -neg
for v, q in adj[u]:
    if p * q > best[v]:
        best[v] = p * q
        heapq.heappush(heap, (-(p * q), v))
```

The last five problems have been about the settle argument, and this is the one
where it is worth noticing what the argument does not say. A node popped with
product `p` is final because every other route to it still in the heap starts
from some `q <= p` and can only be multiplied by factors in `[0, 1]` from here
on. Nothing in that mentions addition. What carries it is that the update never
improves a value, and `* q` for `q <= 1` is non-improving for the same reason
`+ w` for `w >= 0` is.

So the relation here is `best[u] * q == best[v]`, and it is the problem's
relation. That is the correction the 19th ended on, arriving at a problem where
the arithmetic changes and the argument does not.

## The tie-break does not matter, and there was plenty to break

`flip` breaks heap ties on the larger id, the same knob 1786 and 3123 used. The
oracle enumerates every simple path and keeps the best exact product and how
many paths attain it, so the tied graphs can be counted rather than assumed.

| n | probabilities | graphs | reachable | tied best routes | dijkstra wrong | flipped wrong |
|---|---|---|---|---|---|---|
| 3 | 1/4, 1/2, 1 | 64 | 57 | 6 | 0 | 0 |
| 4 | 1/4, 1/2, 1 | 4096 | 3954 | 920 | 0 | 0 |
| 5 | 1/2, 1 | 59049 | 57354 | 27279 | 0 | 0 |

Every simple graph, connected or not, exact rational arithmetic throughout.
27279 of the n = 5 graphs have two or more routes attaining the best product and
the tie-break moves the answer on none of them.

That is the whole difference from the last two problems, and it is not about
graphs. In 1786 the heap decided whether a *count* was wrong. In 3123 it decided
which of the tied edges a *set* kept. Here what is returned is one number, and a
tie is by definition two routes carrying the same number, so there is nothing
for the choice to change. The tie-break can only matter to an answer that can
tell the tied objects apart.

## Floats: not the rounding

Every simple graph at n = 4 with probabilities from `0.1, 0.3, 0.9`, float
Dijkstra against the exact rational answer:

| graphs | float not exactly equal | off by >1e-9 | off by >1e-6 | worst gap |
|---|---|---|---|---|
| 4096 | 3954 | 0 | 0 | 1.110e-16 |

and on 1000 random graphs each at n = 10:

| m | probabilities | product form, worst gap | -log form, worst gap | the two disagree |
|---|---|---|---|---|
| 12 | 0.1, 0.3, 0.9 | 1.110e-16 | 1.110e-16 | 516/1000 |
| 25 | 0.1, 0.3, 0.9 | 2.220e-16 | 1.110e-16 | 333/1000 |
| 25 | 0.99 | 1.110e-16 | 0.000e+00 | 12/1000 |
| 25 | 0, 0.5, 1 | 0.000e+00 | 2.776e-17 | 4/1000 |

The two forms disagree in their last bits about half the time and neither is
ever off by more than 2.2e-16, against a judge that allows 1e-5. Rounding is not
where this breaks.

## Where it does break: a long chain

A single path of `L` edges all of probability `p`, which is the shape the
statement's `n = 10^4` allows.

| p | what the product form does | true value there |
|---|---|---|
| 0.5 | reaches 0 at 1075 edges | 1e-324 |
| 0.9 | never reaches 0 below 20000, pinned in the subnormals at 2.470e-323 | 1e-915 at 20000 |
| 0.99 | still an ordinary float at 20000 edges, 5.057e-88 | 1e-87 |

Halving marches to zero because every step is exact. Multiplying by 0.9 does
not: once the value is subnormal each product rounds back up to where it
started, and `x * 0.9 == x` becomes true at `2.47e-323`. The result is a fixed
point, not an underflow, and it is a nonzero garbage value about 10^592 too
large.

| edges | 0.9 | 0.8 | true | -log costs |
|---|---|---|---|---|
| 2000 | 3.055e-92 | 1.513e-194 | 1e-92, 1e-194 | 210.7, 446.3 |
| 10000 | 2.470e-323 | 9.881e-324 | 1e-458, 1e-969 | 1053.6, 2231.4 |

At 10000 edges the product form puts the two chains two subnormal steps apart
when they are 511 orders of magnitude apart, so it has kept the ordering by
luck and lost the ability to compare. The `-log` form is still accurate to
4.5e-11 in the cost, and it loses everything at the same place if you
exponentiate: `exp(-1053.6)` is 0. The ordering survives only as long as you do
not ask for the probability back. None of this is visible to the judge, which
accepts 0 for both.

## Probabilities above 1, which the statement forbids

Allowing `3/2` as a factor is the direct test of what the settle argument was
resting on. Against the best *simple* path, since with factors above 1 a cycle
makes the best walk unbounded:

| n | | graphs | wrong | too big | too small |
|---|---|---|---|---|---|
| 4 | as written | 729 | 166 | 153 | 13 |
| 4 | with the done check | 729 | 13 | 0 | 13 |
| 5 | as written | 59049 | 20315 | 16897 | 3418 |
| 5 | with the done check | 59049 | 5582 | 0 | 5582 |

The too-small half is the settle argument failing, which is what was expected:
a node is finalized and a better route arrives later. The too-big half is not
about the settle at all. The relaxation writes into `best[v]` without asking
whether `v` is already done, so a settled node's value can be overwritten by a
route that goes back through it. The smallest one is two edges:

```
0 -- 3  at 1/2,   2 -- 3  at 3/2
```

The answer is `1/2`. Dijkstra returns `9/8`, along `0 -> 3 -> 2 -> 3`. Adding
`if done[v]: continue` removes all 16897 of those and leaves only the honest
failure. Inside the statement's `[0, 1]` no such write can ever land, so the
missing check costs nothing and is invisible, which is why it was there to find.

## At the statement's size

`n = 10000` with 20000 and 10000 random edges: 0.03s and under 0.01s, the
product and `-log` forms agreeing to 1e-17 and 5e-20.

## What I had wrong

Five predictions written before the run.

- **Right:** the settle argument survives the change from a sum to a product,
  wrong on none of the 63209 exhaustive graphs. The tie-break cannot matter
  because the answer is a scalar, and it did not, on 27279 tied graphs.
- **Wrong:** that float rounding would be the interesting failure. It never
  exceeds 2.2e-16 anywhere reachable.
- **Wrong:** that a chain of 0.9 underflows to zero around 7000 edges. It
  reaches a fixed point in the subnormals instead and never returns 0 at all.
- **Wrong:** that with factors above 1 the answer could only be too small. It
  is too big 153 times of 166 at n = 4, and that half is a missing `done` check
  rather than the settle argument, which the guarded column separates out.

## Bounds

`O(m log n)` and `O(n + m)`, one pop per node and one push per improvement. The
answer is in `[0, 1]` and is 0 exactly when no path avoids a zero-probability
edge. The `-log` form costs two transcendental calls per edge and buys back
about 400 orders of magnitude of range.

## Files

- `python/solution.py`
