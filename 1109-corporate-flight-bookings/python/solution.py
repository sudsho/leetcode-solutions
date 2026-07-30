class Solution:
    def corpFlightBookings(self, bookings, n):
        # the naive read is "add seats to every flight in [first, last]", which is
        # O(n) per booking. but a range add is exactly the thing a difference
        # array makes O(1): store the CHANGE between neighbours instead of the
        # values, and a whole range shifts by touching only its two endpoints.
        #
        # this is the prefix-sum map run backwards. all month the pattern was
        # values -> prefix sums to answer range queries; here it is range updates
        # -> differences, and the prefix sum is what undoes it at the end.
        diff = [0] * (n + 1)  # one extra slot so last == n needs no bounds check

        for first, last, seats in bookings:
            # flights are 1-indexed, the array is 0-indexed, so flight f lives at
            # f - 1. the +seats says "from here on, seats more than before".
            diff[first - 1] += seats
            # and the -seats at last (not last - 1) cancels it starting at the
            # flight AFTER the range. off-by-one here is the whole problem: index
            # last is the first flight that should not receive the seats.
            diff[last] -= seats

        # running sum of the changes rebuilds the actual per-flight totals. every
        # booking that opened at or before i and has not closed yet is still in
        # the sum, which is precisely the set of bookings covering flight i.
        answer = []
        running = 0
        for i in range(n):
            running += diff[i]
            answer.append(running)

        # the extra slot at diff[n] is never read - it only ever absorbs the
        # closing -seats of bookings that run to the last flight.
        return answer
