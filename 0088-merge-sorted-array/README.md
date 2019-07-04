# 88. Merge Sorted Array

Difficulty: Easy
Topics: two pointers, array

## Problem

Merge nums2 into nums1 in place. nums1 has enough trailing zero slots to fit nums2. Both arrays are sorted ascending.

## Approach

Fill nums1 from the back. Use three pointers: end of nums1 real values (m-1), end of nums2 (n-1), and write index (m+n-1). Pick the larger and write.

## Complexity

Time O(n+m), space O(1).

## Files

- `python/solution.py`
