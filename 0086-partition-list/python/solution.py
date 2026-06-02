class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt


class Solution:
    def partition(self, head, x):
        less_head = ListNode()
        more_head = ListNode()
        less = less_head
        more = more_head

        cur = head
        while cur:
            if cur.val < x:
                less.next = cur
                less = cur
            else:
                more.next = cur
                more = cur
            cur = cur.next

        more.next = None
        less.next = more_head.next
        return less_head.next
