import random
from typing import Dict, List

class RandomizedSet:
    def __init__(self) -> None:
        self.vals: List[int] = []
        self.idx: Dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.idx:
            return False
        self.idx[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.idx:
            return False
        i = self.idx[val]
        last = self.vals[-1]
        self.vals[i] = last
        self.idx[last] = i
        self.vals.pop()
        del self.idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)
