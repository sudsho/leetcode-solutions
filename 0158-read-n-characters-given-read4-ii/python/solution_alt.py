from typing import List

def read4(buf4: List[str]) -> int: ...

class Solution:
    def __init__(self) -> None:
        self.buffer = [""] * 4
        self.head = 0
        self.tail = 0

    def read(self, buf: List[str], n: int) -> int:
        i = 0
        while i < n:
            if self.head == self.tail:
                self.tail = read4(self.buffer)
                self.head = 0
                if self.tail == 0:
                    break
            while i < n and self.head < self.tail:
                buf[i] = self.buffer[self.head]
                i += 1
                self.head += 1
        return i

# revisit: minor renames and one early exit added
