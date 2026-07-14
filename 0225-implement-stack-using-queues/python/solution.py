from collections import deque


class MyStack:
    """LIFO stack backed by a single FIFO queue.

    The trick: keep the queue ordered so its front is always the most
    recently pushed element. After enqueuing a new value we rotate every
    older element behind it, so the newest sits at the front ready to pop.
    That makes push O(n) and pop/top O(1).
    """

    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        # rotate the older elements to sit behind the new one
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return not self.q
