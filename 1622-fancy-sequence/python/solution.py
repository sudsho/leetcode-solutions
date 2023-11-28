class Fancy:
    MOD = 10 ** 9 + 7
    def __init__(self):
        self.seq: list[int] = []
        self.a = 1
        self.b = 0
    def append(self, val: int) -> None:
        # store v as raw, but we want a * raw + b == val => raw = (val - b) * inv(a)
        inv_a = pow(self.a, -1, Fancy.MOD)
        self.seq.append((val - self.b) * inv_a % Fancy.MOD)
    def addAll(self, inc: int) -> None:
        self.b = (self.b + inc) % Fancy.MOD
    def multAll(self, m: int) -> None:
        self.a = self.a * m % Fancy.MOD
        self.b = self.b * m % Fancy.MOD
    def getIndex(self, idx: int) -> int:
        if idx >= len(self.seq):
            return -1
        return (self.a * self.seq[idx] + self.b) % Fancy.MOD
