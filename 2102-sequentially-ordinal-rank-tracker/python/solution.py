import heapq

class SORTracker:
    def __init__(self):
        # left: max-heap of (score, neg name) for top i items
        # right: min-heap for the rest
        self.left: list = []
        self.right: list = []
        self.q = 0

    def add(self, name: str, score: int) -> None:
        # push to left first then balance
        heapq.heappush(self.left, (score, self._neg(name)))
        if len(self.left) > self.q + 1:
            s, nn = heapq.heappop(self.left)
            heapq.heappush(self.right, (-s, self._un(nn)))

    def get(self) -> str:
        s, nn = self.left[0]
        ans = self._un(nn)
        # promote next from right after returning
        self.q += 1
        if self.right:
            rs, rn = heapq.heappop(self.right)
            heapq.heappush(self.left, (-rs, self._neg(rn)))
        return ans

    @staticmethod
    def _neg(s: str) -> tuple:
        return tuple(-ord(c) for c in s)

    @staticmethod
    def _un(t: tuple) -> str:
        return ''.join(chr(-x) for x in t)
# revisit
