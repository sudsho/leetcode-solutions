# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeElements(self, head, val):
        """Remove every node whose value equals `val`.

        The awkward part of a plain traversal is the head itself: if the list
        starts with one or more nodes equal to `val`, there is no predecessor to
        re-link. A dummy node sitting in front of the real head removes that
        special case entirely. `prev` trails one node behind `cur`; whenever
        `cur` matches we splice it out by pointing `prev.next` past it, and only
        advance `prev` when we keep a node. Returning `dummy.next` gives the new
        head, which may differ from the original.
        """
        dummy = ListNode(0, head)
        prev = dummy
        cur = head
        while cur:
            if cur.val == val:
                prev.next = cur.next  # drop cur, prev stays put
            else:
                prev = cur            # keep cur, prev moves up
            cur = cur.next
        return dummy.next
