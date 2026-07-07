import heapq


class Solution:
    def kClosest(self, points, k):
        """Return the k points nearest the origin.

        Keep a max-heap of size k keyed on squared distance. We push the
        negated distance so Python's min-heap behaves as a max-heap: the
        farthest of the current k sits at the top and gets evicted the
        moment a closer point shows up. No need for real distances - the
        square root is monotonic, so comparing x*x + y*y preserves order
        while avoiding float error.
        """
        heap = []  # holds (-dist2, x, y), at most k entries
        for x, y in points:
            dist2 = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist2, x, y))
            elif -dist2 > heap[0][0]:
                # closer than the current farthest -> swap it in
                heapq.heapreplace(heap, (-dist2, x, y))
        return [[x, y] for _, x, y in heap]


class SolutionQuickselect:
    def kClosest(self, points, k):
        """O(n) average alternative via quickselect.

        Partition around a pivot distance until the k closest points land
        in the left slice, then return that slice. Worst case is O(n^2) if
        pivots keep splitting badly, but on random data it beats the heap.
        """
        dist = lambda p: p[0] * p[0] + p[1] * p[1]

        def partition(lo, hi):
            pivot = dist(points[hi])
            store = lo
            for i in range(lo, hi):
                if dist(points[i]) < pivot:
                    points[store], points[i] = points[i], points[store]
                    store += 1
            points[store], points[hi] = points[hi], points[store]
            return store

        lo, hi = 0, len(points) - 1
        while lo < hi:
            p = partition(lo, hi)
            if p == k:
                break
            elif p < k:
                lo = p + 1
            else:
                hi = p - 1
        return points[:k]


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.kClosest([[1, 3], [-2, 2]], 1)) == [[-2, 2]]
    got = sorted(s.kClosest([[3, 3], [5, -1], [-2, 4]], 2))
    assert got == [[-2, 4], [3, 3]], got
    print("ok")
