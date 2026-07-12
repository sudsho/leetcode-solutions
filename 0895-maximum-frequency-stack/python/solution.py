from collections import defaultdict


class FreqStack:
    def __init__(self):
        # how many times each value is currently in the stack
        self.freq = defaultdict(int)
        # freq f -> stack of values that have reached count f
        self.groups = defaultdict(list)
        # the highest freq any value currently has
        self.maxfreq = 0

    def push(self, val):
        self.freq[val] += 1
        f = self.freq[val]
        if f > self.maxfreq:
            self.maxfreq = f
        # record that val is now (at least) f-frequent; later pushes of the
        # same value land in higher groups, so each group keeps its own order
        self.groups[f].append(val)

    def pop(self):
        # the most frequent value is always on top of the maxfreq group, and
        # ties break toward the most recently pushed one for free
        val = self.groups[self.maxfreq].pop()
        self.freq[val] -= 1
        if not self.groups[self.maxfreq]:
            self.maxfreq -= 1
        return val
