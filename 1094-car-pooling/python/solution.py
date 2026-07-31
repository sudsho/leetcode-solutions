class Solution:
    def carPooling(self, trips, capacity):
        # the difference array again, and this time the accumulated value is
        # neither a total to return (1109) nor a yes/no cover flag (2848) - it
        # is a live quantity that has to stay under a bound at every point. so
        # the check goes INSIDE the accumulation loop and bails on the first
        # violation, rather than after it.
        MAX_LOCATION = 1000
        diff = [0] * (MAX_LOCATION + 1)

        for passengers, start, end in trips:
            # the ranges here are half-open in disguise: passengers get off AT
            # end, so the car is empty for them from end onwards. that means
            # -passengers at end, not end + 1. this is the one place the
            # inclusive-range habit from 1109 and 2848 actively misleads - the
            # off-by-one is decided by the problem's semantics, not the
            # technique's.
            diff[start] += passengers
            diff[end] -= passengers

        # walk the route once. onboard is the actual occupancy at each stop,
        # and drop-offs are already netted against pickups at a shared location
        # because both wrote into the same slot - which is exactly the "get off
        # before others get on" rule the problem wants, for free.
        onboard = 0
        for location in range(MAX_LOCATION + 1):
            onboard += diff[location]
            if onboard > capacity:
                return False

        return True

    def carPoolingHeap(self, trips, capacity):
        """Alt: sort trips by pickup and evict finished ones with a min-heap.

        The version that does not care how long the route is - it scales with
        the number of trips instead of the coordinate range, which is what you
        need once locations stop being bounded by 1000. Same idea underneath:
        the heap is just tracking which range updates are still open.
        """
        import heapq

        onboard = 0
        active = []  # (drop-off location, passenger count) still in the car

        for passengers, start, end in sorted(trips, key=lambda t: t[1]):
            # anyone whose drop-off is at or before this pickup has already
            # left. <= and not < because passengers exit before boarding.
            while active and active[0][0] <= start:
                _, leaving = heapq.heappop(active)
                onboard -= leaving

            onboard += passengers
            if onboard > capacity:
                return False
            heapq.heappush(active, (end, passengers))

        return True
