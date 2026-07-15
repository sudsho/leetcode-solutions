class Solution:
    def oddEvenList(self, head):
        """Group nodes at odd indices before nodes at even indices, in place.

        Weave two sublists as we walk: `odd` collects 1st, 3rd, 5th... nodes,
        `even` collects 2nd, 4th... . Keep a handle on the even head so we can
        stitch it onto the tail of the odd list at the end. O(n) time, O(1)
        space, and the relative order inside each group is preserved.
        """
        if head is None or head.next is None:
            return head

        odd = head
        even = head.next
        even_head = even  # where the odd tail will reconnect

        while even and even.next:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next

        odd.next = even_head
        return head
