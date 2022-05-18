# pre-flatten on construction
from typing import List

class NestedInteger:
    def isInteger(self) -> bool: ...
    def getInteger(self) -> int: ...
    def getList(self) -> List["NestedInteger"]: ...

class NestedIterator:
    def __init__(self, nestedList: List[NestedInteger]) -> None:
        self.flat: List[int] = []
        self._flatten(nestedList)
        self.idx = 0

    def _flatten(self, lst: List[NestedInteger]) -> None:
        for x in lst:
            if x.isInteger():
                self.flat.append(x.getInteger())
            else:
                self._flatten(x.getList())

    def next(self) -> int:
        v = self.flat[self.idx]
        self.idx += 1
        return v

    def hasNext(self) -> bool:
        return self.idx < len(self.flat)
