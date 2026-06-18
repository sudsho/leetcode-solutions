# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head):
        """Remove every node that has a duplicate, leaving only distinct values.

        Unlike problem 83 (which keeps one copy), here a value that appears more
        than once is deleted entirely. A dummy node in front lets us drop runs
        that start at the head without special-casing. `prev` always points at
        the last node known to be unique; when `cur` begins a duplicate run we
        skip the whole run and splice `prev` straight to whatever follows it.
        """
        dummy = ListNode(0, head)
        prev = dummy
        cur = head
        while cur:
            if cur.next and cur.val == cur.next.val:
                # advance to the end of the run of equal values
                while cur.next and cur.val == cur.next.val:
                    cur = cur.next
                prev.next = cur.next  # unlink the entire run
            else:
                prev = cur
            cur = cur.next
        return dummy.next
