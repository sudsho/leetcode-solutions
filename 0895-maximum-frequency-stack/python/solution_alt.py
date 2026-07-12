# alt approach: max-heap keyed on (frequency, insertion order)
# slower at O(log n) per op vs the O(1) grouped-stacks version, kept for reference
import heapq
from collections import defaultdict


class FreqStack:
    def __init__(self):
        self.freq = defaultdict(int)
        self.heap = []
        # monotonic counter so that among equal frequencies the newest wins
        self.seq = 0

    def push(self, val):
        self.freq[val] += 1
        # negate both keys so python's min-heap behaves like a max-heap:
        # highest frequency first, and within a frequency the largest seq
        heapq.heappush(self.heap, (-self.freq[val], -self.seq, val))
        self.seq += 1

    def pop(self):
        _, _, val = heapq.heappop(self.heap)
        self.freq[val] -= 1
        return val
