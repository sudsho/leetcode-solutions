# trie uses

- track entry seen in trie alongside word counts.
- early return when source == target. cheap, easy to forget.
- recurse on `n - n//2 - 1` for the right subtree count.
