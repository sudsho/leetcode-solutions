# hash-set version - clearer for learning
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

class Solution:
    def getIntersectionNode(self, headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        node = headA
        while node:
            seen.add(id(node))
            node = node.next
        node = headB
        while node:
            if id(node) in seen:
                return node
            node = node.next
        return None
