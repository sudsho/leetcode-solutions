from bisect import bisect_left, bisect_right
from heapq import heappush, heappop


class Solution:
    def fullBloomFlowers(self, flowers, people):
        # this is the difference array again, except the coordinate space is
        # 10^9 wide so there is no array to allocate. the way out is to notice
        # what the accumulate was actually computing: the value at position t
        # is the prefix sum of the diff array up to t, which is
        # (number of +1 events at or before t) - (number of -1 events at or
        # before t). neither of those needs the array - they are just counts in
        # two sorted lists, and a count in a sorted list is a binary search.
        starts = sorted(f[0] for f in flowers)
        ends = sorted(f[1] for f in flowers)

        result = []
        for t in people:
            # bloom is inclusive on both sides, so a flower is open at t when
            # start <= t <= end. bisect_right on starts counts start <= t;
            # bisect_left on ends counts end < t, i.e. the ones already closed.
            # the two different bisects are the same inclusive-vs-half-open
            # decision the closing write encodes in the array version - get it
            # backwards and every flower wilting exactly at t gets dropped.
            opened = bisect_right(starts, t)
            closed = bisect_left(ends, t)
            result.append(opened - closed)

        return result

    def fullBloomFlowersSweep(self, flowers, people):
        """Offline sweep: sort the people and walk the events once.

        Same answer by the other route. Instead of querying the prefix sum at
        arbitrary points, sort the queries so the sweep can be resumed - the
        classic offline trade. The heap holds the flowers that have opened and
        not yet closed, which is literally the set of unaccumulated +1s the
        array version would be carrying in its running total.

        Kept because it is the version that generalizes: if the query were
        "which flowers", not "how many", the binary-search count gives nothing
        and this one hands you the open set directly.
        """
        flowers = sorted(flowers)
        order = sorted(range(len(people)), key=lambda i: people[i])

        result = [0] * len(people)
        open_ends = []  # min-heap of end times of currently-blooming flowers
        i = 0

        for idx in order:
            t = people[idx]
            # open every flower that has started by t
            while i < len(flowers) and flowers[i][0] <= t:
                heappush(open_ends, flowers[i][1])
                i += 1
            # retire every flower that finished strictly before t. <= would be
            # wrong for the same reason bisect_left is right above: a flower
            # ending at t is still blooming at t.
            while open_ends and open_ends[0] < t:
                heappop(open_ends)
            result[idx] = len(open_ends)

        return result

    def fullBloomFlowersNaive(self, flowers, people):
        """O(n * m) check, for reference.

        With n and m both up to 5 * 10^4 this is 2.5 billion comparisons, which
        is the whole reason the sorted structure exists.
        """
        return [
            sum(1 for start, end in flowers if start <= t <= end)
            for t in people
        ]
