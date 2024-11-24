class MyCalendarThree:
    # Segment tree with lazy propagation
    def __init__(self):
        self.tree: dict[int, int] = {}
        self.lazy: dict[int, int] = {}

    def update(self, node: int, lo: int, hi: int, ql: int, qr: int) -> None:
        if qr <= lo or hi <= ql:
            return
        if ql <= lo and hi <= qr:
            self.tree[node] = self.tree.get(node, 0) + 1
            self.lazy[node] = self.lazy.get(node, 0) + 1
            return
        mid = (lo + hi) // 2
        self.update(2 * node, lo, mid, ql, qr)
        self.update(2 * node + 1, mid, hi, ql, qr)
        self.tree[node] = self.lazy.get(node, 0) + max(
            self.tree.get(2 * node, 0), self.tree.get(2 * node + 1, 0)
        )

    def book(self, startTime: int, endTime: int) -> int:
        self.update(1, 0, 10 ** 9, startTime, endTime)
        return self.tree.get(1, 0)
