# straightforward bfs by levels with queue
from typing import Optional
from collections import deque

class Node:
    def __init__(self, val: int = 0, left: Optional["Node"] = None, right: Optional["Node"] = None, next: Optional["Node"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution:
    def connect(self, root: Optional[Node]) -> Optional[Node]:
        if root is None:
            return None
        q = deque([root])
        while q:
            sz = len(q)
            prev: Optional[Node] = None
            for _ in range(sz):
                node = q.popleft()
                if prev:
                    prev.next = node
                prev = node
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return root
