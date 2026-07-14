# 211. Design Add and Search Words Data Structure

Difficulty: Medium
Topics: trie, dfs, design, string

## Problem

Design a data structure supporting `addWord(word)` and `search(word)`. In `search`, a `.` can match any single letter. Return whether some added word matches.

## Approach

Store words in a trie. `addWord` walks down creating nodes. `search` is a DFS over the trie: a normal character follows the one matching child, a `.` recurses into every child. The `end` flag marks a complete word so we only match full words, not prefixes.

## Complexity

`addWord` O(L). `search` O(L) with no wildcards; worst case O(26^L) when the query is all dots. Space O(total characters added).

## Files

- `python/solution.py`
