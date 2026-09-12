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
  that is for reachability only. counting shortest sequences, the rescan reaches
  a `+=` and the clear (or a `farthest` pointer) is the wrong answer (1345, 1871).
- dijkstra stale skip (`if d > dist[u]: continue`): plain dijkstra survives
  losing it, which says nothing about the program in front of you. go through
  each update the pop reaches and ask whether a repeat is absorbed under what it
  reads - strict `<` and max are, an overwrite only from dist[u], `+=` and a
  per-pop counter never (1976, 882).
