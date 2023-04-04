from collections import defaultdict
from typing import List

class Excel:
    def __init__(self, height: int, width: str):
        self.cells: dict[tuple[int, int], int] = {}
        self.formulas: dict[tuple[int, int], list[tuple[int, int]]] = {}
    def set(self, row: int, column: str, val: int) -> None:
        c = (row, ord(column) - 64)
        self.cells[c] = val
        self.formulas.pop(c, None)
    def get(self, row: int, column: str) -> int:
        c = (row, ord(column) - 64)
        if c in self.formulas:
            total = 0
            for ref in self.formulas[c]:
                total += self.get(*self._key_to_pair(ref))
            return total
        return self.cells.get(c, 0)
    def sum(self, row: int, column: str, numbers: List[str]) -> int:
        c = (row, ord(column) - 64)
        refs: list[tuple[int, int]] = []
        for spec in numbers:
            if ':' in spec:
                a, b = spec.split(':')
                r1, c1 = int(a[1:]), ord(a[0]) - 64
                r2, c2 = int(b[1:]), ord(b[0]) - 64
                for r in range(r1, r2 + 1):
                    for col in range(c1, c2 + 1):
                        refs.append((r, col))
            else:
                refs.append((int(spec[1:]), ord(spec[0]) - 64))
        self.formulas[c] = refs
        return self.get(row, column)
    @staticmethod
    def _key_to_pair(k: tuple[int, int]) -> tuple[int, str]:
        return k[0], chr(64 + k[1])
