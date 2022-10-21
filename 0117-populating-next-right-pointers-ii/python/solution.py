from typing import Optional

class Node:
    def __init__(self, val: int = 0, left: Optional["Node"] = None, right: Optional["Node"] = None, next: Optional["Node"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution:
    def connect(self, root: Optional[Node]) -> Optional[Node]:
        node = root
        while node:
            dummy = Node()
            tail = dummy
            curr = node
            while curr:
                if curr.left:
                    tail.next = curr.left
                    tail = tail.next
                if curr.right:
                    tail.next = curr.right
                    tail = tail.next
                curr = curr.next
            node = dummy.next
        return root
