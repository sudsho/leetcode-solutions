class Solution:
    def isSelfCrossing(self, distance):
        """Walk north/west/south/east with the given step lengths and decide if
        the path ever crosses itself. Only three local crossing patterns exist;
        checking them against the last few edges is enough (O(1) memory)."""
        d = distance
        n = len(d)
        for i in range(3, n):
            # Case 1: current edge crosses the one 3 steps back (a tight spiral
            # that closes on itself).
            if d[i] >= d[i - 2] and d[i - 1] <= d[i - 3]:
                return True
            # Case 2: current edge touches the edge 4 back (overlap).
            if i >= 4 and d[i - 1] == d[i - 3] and d[i] + d[i - 4] >= d[i - 2]:
                return True
            # Case 3: crossing involving the edge 5 back.
            if (i >= 5 and d[i - 2] >= d[i - 4] and d[i] + d[i - 4] >= d[i - 2]
                    and d[i - 1] <= d[i - 3] and d[i - 1] + d[i - 5] >= d[i - 3]):
                return True
        return False
