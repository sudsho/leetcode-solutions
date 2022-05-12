from typing import List

class NestedInteger:
    def isInteger(self) -> bool: ...
    def getInteger(self) -> int: ...
    def getList(self) -> List["NestedInteger"]: ...

class NestedIterator:
    def __init__(self, nestedList: List[NestedInteger]) -> None:
        self.stack = [iter(nestedList)]

    def next(self) -> int:
        self.hasNext()
        return self._top.getInteger()

    def hasNext(self) -> bool:
        while self.stack:
            try:
                v = next(self.stack[-1])
            except StopIteration:
                self.stack.pop()
                continue
            if v.isInteger():
                self._top = v
                self.stack.append(iter([v]))
                next(self.stack[-1])
                return True
            self.stack.append(iter(v.getList()))
        return False
