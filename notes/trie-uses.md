# trie uses

- track entry seen in trie alongside word counts.
- early return when source == target. cheap, easy to forget.
- recurse on `n - n//2 - 1` for the right subtree count.
- monotonic stack: keep indexes, not values, when you might need positions.
- meet in the middle for subset closest sum.
- monotonic deque for sliding window minimum.
- segment tree with coordinate compression for range count problems.
