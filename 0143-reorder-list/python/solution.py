class Solution:
    def reorderList(self, head):
        """Reorder L0->L1->...->Ln-1->Ln into L0->Ln->L1->Ln-1->...

        Three phases, all O(1) extra space:
          1. find the middle with slow/fast pointers
          2. reverse the second half in place
          3. weave the two halves together node by node
        """
        if head is None or head.next is None:
            return

        # 1. midpoint: slow ends at the start of the second half
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. reverse second half, then cut the first half loose
        second = slow.next
        slow.next = None
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt
        second = prev

        # 3. interleave first and reversed-second halves
        first = head
        while second:
            f_next, s_next = first.next, second.next
            first.next = second
            second.next = f_next
            first, second = f_next, s_next
