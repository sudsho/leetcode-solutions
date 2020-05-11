class Solution:
    def merge(self, intervals):
        intervals.sort(key=lambda x: x[0])
        out = []
        for iv in intervals:
            if out and iv[0] <= out[-1][1]:
                out[-1][1] = max(out[-1][1], iv[1])
            else:
                out.append(iv[:])
        return out
