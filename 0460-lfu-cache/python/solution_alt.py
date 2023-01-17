# 2023 nit (7)
# alt: linked-list per frequency (more allocation overhead)
from collections import defaultdict
from typing import Dict

class Node:
    __slots__ = ("k", "v", "freq", "prev", "next")

    def __init__(self, k: int = 0, v: int = 0, freq: int = 0) -> None:
        self.k = k
        self.v = v
        self.freq = freq
        self.prev: "Node" = None  # type: ignore
        self.next: "Node" = None  # type: ignore

class DoubleList:
    def __init__(self) -> None:
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_back(self) -> Node:
        node = self.tail.prev
        self.remove(node)
        return node

class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: Dict[int, Node] = {}
        self.lists: Dict[int, DoubleList] = defaultdict(DoubleList)
        self.min_freq = 0

    def _bump(self, node: Node) -> None:
        f = node.freq
        self.lists[f].remove(node)
        if self.lists[f].size == 0 and f == self.min_freq:
            self.min_freq += 1
        node.freq += 1
        self.lists[node.freq].add_front(node)

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._bump(node)
        return node.v

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return
        if key in self.map:
            node = self.map[key]
            node.v = value
            self._bump(node)
            return
        if len(self.map) == self.cap:
            evict = self.lists[self.min_freq].pop_back()
            del self.map[evict.k]
        node = Node(key, value, 1)
        self.map[key] = node
        self.lists[1].add_front(node)
        self.min_freq = 1
