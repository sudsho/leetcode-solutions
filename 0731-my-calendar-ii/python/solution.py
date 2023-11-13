class MyCalendarTwo:
    def __init__(self):
        self.bookings: list[tuple[int, int]] = []
        self.overlaps: list[tuple[int, int]] = []
    def book(self, startTime: int, endTime: int) -> bool:
        for s, e in self.overlaps:
            if startTime < e and s < endTime:
                return False
        for s, e in self.bookings:
            if startTime < e and s < endTime:
                self.overlaps.append((max(s, startTime), min(e, endTime)))
        self.bookings.append((startTime, endTime))
        return True
