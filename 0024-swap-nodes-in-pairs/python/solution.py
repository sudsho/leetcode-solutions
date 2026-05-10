from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # iterative with a dummy node so we don't special-case the head swap
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a = prev.next
            b = a.next
            # before:  prev -> a -> b -> rest
            # after:   prev -> b -> a -> rest
            a.next = b.next
            b.next = a
            prev.next = b
            prev = a
        return dummy.next

    def swapPairsRecursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        nxt = head.next
        head.next = self.swapPairsRecursive(nxt.next)
        nxt.next = head
        return nxt
