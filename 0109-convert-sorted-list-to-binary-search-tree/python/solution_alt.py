# divide and conquer using slow/fast pointer
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        def find_mid(node: Optional[ListNode]) -> Optional[ListNode]:
            slow = fast = node
            prev: Optional[ListNode] = None
            while fast and fast.next:
                prev = slow
                slow = slow.next
                fast = fast.next.next
            if prev:
                prev.next = None
            return slow

        def build(node: Optional[ListNode]) -> Optional[TreeNode]:
            if node is None:
                return None
            mid = find_mid(node)
            if mid is None:
                return None
            root = TreeNode(mid.val)
            if node is mid:
                return root
            root.left = build(node)
            root.right = build(mid.next)
            return root
        return build(head)
