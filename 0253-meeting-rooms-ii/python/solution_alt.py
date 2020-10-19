# sweep line / chronological ordering
class Solution:
    def minMeetingRooms(self, intervals):
        starts = sorted(i[0] for i in intervals)
        ends = sorted(i[1] for i in intervals)
        rooms = 0
        peak = 0
        e = 0
        for s in starts:
            if s < ends[e]:
                rooms += 1
                if rooms > peak:
                    peak = rooms
            else:
                e += 1
        return peak
