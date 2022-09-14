# variation using __getitem__ semantics
import random
from typing import Dict, List

class RandomizedSet:
    def __init__(self) -> None:
        self._a: List[int] = []
        self._where: Dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self._where:
            return False
        self._where[val] = len(self._a)
        self._a.append(val)
        return True

    def remove(self, val: int) -> bool:
        i = self._where.pop(val, -1)
        if i == -1:
            return False
        last = self._a[-1]
        if last != val:
            self._a[i] = last
            self._where[last] = i
        self._a.pop()
        return True

    def getRandom(self) -> int:
        return self._a[random.randrange(len(self._a))]
