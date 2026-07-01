# 424. Longest Repeating Character Replacement

Difficulty: Medium
Topics: string, sliding window, hash map

## Problem

Given a string `s` and an integer `k`, you may replace at most `k` characters
with any uppercase letter. Return the length of the longest substring containing
the same letter you can get after doing so.

## Approach

Sliding window keeping a count of every letter inside it. The window is valid when
`window_size - max_freq <= k`, where `max_freq` is the count of the most common
letter in the window - those are the ones we keep, the rest we replace. Grow the
right edge each step; when the window becomes invalid, slide the left edge by one.

`max_freq` is never decreased on shrink. A stale-high value only prevents the
window from growing past the best seen so far, which is fine since a shorter
answer can never beat it.

## Complexity

Time O(n), space O(26) for the letter counts.

## Files

- `python/solution.py`
