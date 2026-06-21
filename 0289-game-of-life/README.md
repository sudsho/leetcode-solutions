# 289. Game of Life

Difficulty: Medium
Topics: array, matrix, simulation

## Problem

Given an `m x n` board where each cell is `1` (live) or `0` (dead), compute the next state according to Conway's Game of Life rules and apply it **in place**. All cells update simultaneously based on their current neighbours.

## Approach

The simultaneous update is the whole difficulty: writing a new 0/1 into a cell would corrupt the neighbour counts of cells visited later. Use the second bit to carry the next state while the low bit keeps the original:

- `bit 0` = current state, `bit 1` = next state.
- During the sweep, count neighbours with `cell & 1` (always the original value) and set `bit 1` when a cell should be alive next.
- A final pass right-shifts every cell so the next state becomes the only state.

This needs no extra grid, so it runs in O(1) auxiliary space.

## Complexity

Time O(m·n) (a constant 8 neighbour checks per cell), space O(1).

## Files

- `python/solution.py`
