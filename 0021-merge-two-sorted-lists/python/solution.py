# revisited - cleaned up
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# revisited - cleaned up
class Solution:
    def mergeTwoLists(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        # attach whatever is left
        tail.next = l1 if l1 else l2
        return dummy.next
