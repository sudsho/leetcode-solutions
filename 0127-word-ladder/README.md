# 127. Word Ladder

Difficulty: Hard
Topics  : bfs, graph

## Problem

Shortest transformation from beginWord to endWord changing one letter at a time. Each intermediate must be in wordList.

## Approach

BFS, generate neighbors by trying every char swap. Use bidirectional BFS for the alt.

## Complexity

Time O(N * L^2), space O(N * L).

## Files

- `python/solution.py`
