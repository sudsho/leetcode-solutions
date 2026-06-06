class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def rotateRight(self, head, k):
        """Rotate the list to the right by k places. Close the list into a ring,
        compute the new tail (length - k % length steps from the old head), then
        break the ring there. Handles k larger than the length via the modulo."""
        if not head or not head.next or k == 0:
            return head

        # measure length and grab the tail
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        k %= length
        if k == 0:
            return head

        # new tail sits length - k - 1 hops past the head
        tail.next = head  # close into a ring
        steps = length - k
        new_tail = head
        for _ in range(steps - 1):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None
        return new_head
