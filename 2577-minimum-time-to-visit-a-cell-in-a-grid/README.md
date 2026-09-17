# 2577. Minimum Time to Visit a Cell in a Grid

Difficulty: Hard
Topics  : Dijkstra, the wait as a closed form, the marking rule under counting, and what the count counts

## Problem

An `m x n` grid where `grid[i][j]` is the earliest second you may be standing in
that cell. You start at `(0, 0)` at second 0, each move to an adjacent cell takes
one second, and you may move back and forth as much as you like. Return the
earliest second you can be at `(m - 1, n - 1)`, or `-1`.

## Approach

Dijkstra over cells. Standing next to a cell of value `v` at second `t`, the
first candidate is `t + 1`, and if the cell is shut the wait is spent stepping
away and back, which costs two seconds, so the arrival keeps the parity of
`t + 1`:

```python
def arrival(t, value):
    step = t + 1
    if value <= step:
        return step
    return value + ((value - step) & 1)
```

The one place that rule is not available is the corner at second 0, which has no
cell behind it to bounce against. Everywhere else the bounce is free: a cell
entered at `t` was entered from a cell of value at most `t - 1`, which is open
again at `t + 1`. So the whole special case is `can_leave_start`, and if both
cells next to the corner are shut at second 1 nothing ever moves.

## Parity

Every second spent in a cell has the parity of `(i + j)`, since a move changes
`i + j` by one. Asserted on all 50337 reachable cells of the exhaustive set. Two
things follow, and both of them are the night's answer.

The wait bump is the same from every neighbour. All four neighbours of a cell sit
at the other parity, so `(value - t - 1) & 1` does not depend on which one you
came from, and `arrival(t, value)` is nondecreasing in `t`. So the earliest
neighbour gives the earliest arrival.

No two adjacent cells share a second. That is what makes the pull below need no
tie-break.

## The marking rule

```python
if seen[i][j]:
    continue
seen[i][j] = True
best[i][j] = arrival(t, grid[i][j])
```

Marking a cell when it is pushed is the BFS habit, and in a weighted graph it is
the usual way to get a wrong answer. Here it is right.

| shape | top | grids | reachable | waiting cells | push-mark times wrong |
|---|---|---|---|---|---|
| 2x2 | 4 | 64 | 84 | 38 | 0 |
| 2x3 | 4 | 1024 | 2240 | 808 | 0 |
| 3x3 | 3 | 6561 | 29160 | 5589 | 0 |
| 2x4 | 3 | 2187 | 8505 | 1620 | 0 |
| 1x5 | 4 | 256 | 256 | 40 | 0 |

Every grid with `grid[0][0] = 0` and the rest in `1..top`, 10092 of them, checked
against an oracle that takes single steps and never uses the arrival rule, plus
2000 random grids to 6x6. The heap pops in nondecreasing second, so the first
neighbour to reach a cell is its earliest neighbour, and by the parity fact that
is its answer.

Two consequences, both measured rather than argued.

**A tentative second is never written twice.** Zero rewrites over the exhaustive
set and over every random family. The reset that a shortest-path count is
supposed to carry, `ways[v] = ways[u]` when the distance improves, never fires
here, and `count_relax(reset=False)` matches `count_relax(reset=True)` on all
10092 grids.

**So the marking rule saves no pushes at all.** Both programs push each
reachable cell exactly once.

```
  shape       top  pushes(mark)  pushes(settle)  pops(mark)  pops(settle)   mark  settle  answer
  300x300         10         89999           89999       90000         90000  0.14s   0.16s     600
  300x300     100000         89999           89999       90000         90000  0.20s   0.22s   67626
  1000x1000         10        999999          999999     1000000       1000000  1.92s   2.14s    2000
  1000x1000     100000        999999          999999     1000000       1000000  2.94s   3.33s   71532
  1000x1000  1000000000        999999          999999     1000000       1000000  3.11s   3.56s  656468114
```

What it saves is the `done` array and the stale-entry test, about 10% of the
running time, not the factor a marking rule usually buys.

## Under counting

Count the routes that arrive at a cell in its earliest second, where a route is a
sequence of cells and the waiting is folded into the arrival rule.

- **carry the count along the push**: wrong on 28 of 64, 448 of 1024, 3645 of
  6561 and 1215 of 2187, and on all 400 of every random family. The cell is
  written once, by its earliest neighbour, so its count is that one neighbour's
  count and every other neighbour arriving in the same second is dropped. This is
  1871, 1345, 3552 and 2612 again with a heap in front of it.
- **`+=` on a tie at pop, reset on improvement**: right everywhere, and the reset
  is dead code.
- **pull at pop**: right everywhere.

The one shape that never fails is `1x5`, 0 of 256, because a path has one route
into each cell and there is nothing for the copy to drop.

## The pull

```python
for i, j in neighbours(r, c, m, n):
    if done[i][j] and arrival(best[i][j], grid[r][c]) == t:
        total += ways[i][j]
```

Four slots, and the ratio of slots to reachable cells is 3.99 on a 300x300 and a
600x600 grid, the shortfall being the border. A neighbour that is not settled yet
cannot become a predecessor, since its second is at least `t`, and no adjacent
pair shares a second, so its arrival here would be past `t`.

```
  shape       top   cells    slots  ratio  seconds  largest route count digits
  300x300         10   90000   358798   3.99   0.31s                        178
  300x300     100000   90000   358798   3.99   0.48s                         54
  600x600     100000  360000  1437598   3.99   2.02s                        104
```

## What the count is not

The oracle counts walks, and a walk spells out the bouncing. The two numbers are
not the same. On the exhaustive set they agree on 7698 grids and differ on 2394,
and the walk count is never the smaller one, up to 4.7x at one cell of a 2x3.

Waiting is necessary for the gap and not sufficient: 5038 grids hold a waiting
cell and only 2394 of them differ. A grid that never waits never differs,
asserted. Where there is a wait the bounce can be spent against any open
neighbour, and each choice is a different walk with the same arrival, so what
the Dijkstra reports is the number of routes and not the number of ways to
spend the seconds.

## What I had wrong

**Pushes without the marking rule roughly double.** They are identical, 999999
either way, because a tentative second is never rewritten, so nothing stale is
ever pushed.

**The marking rule buys about 30% of the running time.** It is 10%, 1.92s against
2.14s and 3.11s against 3.56s.

**Some grid in the exhaustive set needs the reset.** None does, and neither does
any of the 2000 random grids.

**The copy is wrong on more than half the grids.** It is at 3x3 and 2x4, 56% both,
and under half at 2x2 and 2x3, 44% both, and zero at 1x5. On random grids with a
neighbour of the corner forced open it is 400 of 400 every time, so the exhaustive
rate is reporting how many tiny grids are dead rather than how bad the copy is.

The one I got right before running was the parity argument, which is the reason
the marking rule survives here and the reason it is still wrong under counting.

## Bounds

`0` at the corner, `-1` everywhere else when both cells next to it are shut at
second 1. Otherwise every cell is reachable, and the answer is at least `i + j`
and at most `max(grid) + i + j + 1`, since bouncing at the corner until the
largest value has passed makes every cell open for a straight walk, and the `+1`
is the parity. Both ends are attained in the table above: 2000 against a
manhattan distance of 1998 at `top = 10`, and 656468114 at `top = 10^9`.
Dijkstra over `mn` cells and `4mn` slots, `O(mn log(mn))`, with
each cell pushed once whichever marking rule is used. The pull adds four slots
per cell. The route counts have no modulus because nothing asks for one, and they
reach 178 digits on a 300x300 grid.

## Files

- `python/solution.py`
