# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


class Solution:
    def insertionSortList(self, head):
        """Insertion sort on a singly-linked list.

        Build a fresh sorted list behind a dummy head. For each node pulled off
        the input, walk the sorted part from the dummy until the next node would
        exceed it, then splice it in there. Rescanning from the dummy each time
        keeps the logic simple at O(n^2) worst case.
        """
        dummy = ListNode(0)
        curr = head
        while curr:
            nxt = curr.next
            prev = dummy
            while prev.next and prev.next.val <= curr.val:
                prev = prev.next
            curr.next = prev.next
            prev.next = curr
            curr = nxt
        return dummy.next
