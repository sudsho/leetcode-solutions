class Solution:
    def canAttendMeetings(self, intervals):
        # if you can attend every meeting then no two intervals overlap.
        # sort by start time and a clash is just a meeting that begins
        # before the one right before it has ended.
        intervals.sort(key=lambda iv: iv[0])
        for prev, cur in zip(intervals, intervals[1:]):
            if cur[0] < prev[1]:
                return False
        return True
