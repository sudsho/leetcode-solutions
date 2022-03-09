from collections import OrderedDict, defaultdict
from typing import Dict

class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.size = 0
        self.min_freq = 0
        self.values: Dict[int, int] = {}
        self.freqs: Dict[int, int] = {}
        self.buckets: Dict[int, "OrderedDict[int, int]"] = defaultdict(OrderedDict)

    def _bump(self, key: int) -> None:
        f = self.freqs[key]
        del self.buckets[f][key]
        if not self.buckets[f] and f == self.min_freq:
            self.min_freq += 1
        self.freqs[key] = f + 1
        self.buckets[f + 1][key] = 1

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        self._bump(key)
        return self.values[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.values:
            self.values[key] = value
            self._bump(key)
            return
        if self.size == self.cap:
            evict, _ = self.buckets[self.min_freq].popitem(last=False)
            del self.values[evict]
            del self.freqs[evict]
            self.size -= 1
        self.values[key] = value
        self.freqs[key] = 1
        self.buckets[1][key] = 1
        self.min_freq = 1
        self.size += 1
