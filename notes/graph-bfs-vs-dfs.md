# graph bfs vs dfs

- digit dp: pre-compute place value contributions; saves a layer.
- recurse on `n - n//2 - 1` for the right subtree count.
- monotonic stack: keep indexes, not values, when you might need positions.
- bidirectional bfs: swap fronts when one outgrows the other.
- entry 177: small reminder.
- manacher for longest palindromic substring in linear time.
- union find rollback for offline tasks.
- bfs over an implicit dense graph: hold the equivalence classes as buckets and
  clear a bucket once you expand it. one expansion settles the whole class, so
  the clear cannot change an answer, and without it the scan is quadratic.
  that is for reachability only. counting shortest sequences, copying the pop's
  own count through the clear (or a `farthest` pointer, or a skip pointer) is the
  wrong answer (1345, 1871, 2612), and at zero cost deleting the clear is wrong
  too (3552). keep the clear and fill each count once its level is finished, as
  one sum over the part of that level that reaches it - a window of the level's
  run in 1871, the bucket's sum in 1345 and 3552, and a range of the sorted level
  in 2612, since a reversal undoes itself and a level is one parity. a
  frontier-at-a-time bfs knows when a level is finished for free. only the 0-1
  deque in 3552 needed an argument, that a letter's portals share one level.
- dijkstra stale skip (`if d > dist[u]: continue`): plain dijkstra survives
  losing it, which says nothing about the program in front of you. go through
  each update the pop reaches and ask whether a repeat is absorbed under what it
  reads - strict `<` and max are, an overwrite only from dist[u], `+=` and a
  per-pop counter never (1976, 882).
