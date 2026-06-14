# 629. K Inverse Pairs Array

Difficulty: Hard
Topics: dynamic programming, prefix sum

## Problem

For integers n and k, count the arrays made of the numbers 1..n (each used once) that have exactly k inverse pairs. An inverse pair is a position i < j with a[i] > a[j]. Return the count modulo 1e9 + 7.

## Approach

dp[i][j] = arrangements of i numbers with j inverse pairs. Inserting the largest of i numbers adds 0..i-1 inverse pairs, so dp[i][j] is a window sum over dp[i-1]. Converting the window into a prefix difference gives

    dp[i][j] = dp[i][j-1] + dp[i-1][j] - dp[i-1][j-i]

(omit the last term when j < i). Two rolling rows keep memory at O(k).

## Complexity

Time O(n*k), space O(k).

## Files

- `python/solution.py`
