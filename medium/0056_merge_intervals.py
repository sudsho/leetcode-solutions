# Given an array of intervals, merge all overlapping intervals
# and return an array of the non-overlapping intervals that
# cover all the intervals in the input.

from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]

        for start, end in intervals[1:]:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])

        return merged


# Time: O(n log n) - dominated by sorting
# Space: O(n) - output array in worst case (no overlaps)

if __name__ == "__main__":
    sol = Solution()

    # overlapping intervals collapse into one
    print(sol.merge([[1, 3], [2, 6], [8, 10], [15, 18]]))  # [[1,6],[8,10],[15,18]]

    # all intervals overlap into one
    print(sol.merge([[1, 4], [4, 5]]))  # [[1,5]]

    # no intervals overlap
    print(sol.merge([[1, 2], [3, 4], [5, 6]]))  # [[1,2],[3,4],[5,6]]
